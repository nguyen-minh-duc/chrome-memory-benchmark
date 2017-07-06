#author: shend@chromium.org

import numpy
import matplotlib.pyplot as pyplot
import pandas
import os
pyplot.rcParams['figure.figsize'] = (15, 9)

def read_csv(filename):
    return pandas.read_csv(filename, header=None, names=['time', 'event', 'object', 'address', 'size'], skipinitialspace=True, skipfooter=1)

def get_csv_files(directory):
    csv_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            csv_files.append(os.path.join(directory, filename))
    return csv_files

def parse_object_destuction(table):
    table = table.copy()
    table.loc[table['event'] == 'destruct', 'size'] = -table.loc[table['event'] == 'destruct', 'size'].abs()
    return table

def group_timestamps(table, buckets):
    table = table.copy()
    table['bucketed_time'] = table['time'].apply(lambda t: int(t * buckets))
    return table.groupby(by=['bucketed_time', 'object'])['size'].sum()

def total_memory_used(table):
    table = table.copy()
    return table.unstack(level=1).fillna(0).cumsum().iloc[-1]

def normalized_total_memory_used(table, size_of_node):
    table = table.copy()
    table = total_memory_used(table)
    table = table/table['Node']*size_of_node
    return table

def get_csv_files(directory):
    csv_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            csv_files.append(os.path.join(directory, filename))
    return csv_files


def read_individual_csv(filename):
    table = read_csv(filename)
    size_of_node = table[table['object'] == 'Node'].iloc[0]["size"]
    table = group_timestamps(parse_object_destuction(table), 1000) 
    normalized_total_memory_used(table, size_of_node).order(ascending='true').plot(kind='bar')
    pyplot.xlabel('Objects')
    pyplot.ylabel('Memory in bytes')
    pyplot.title('Graph of objects vs memory for google.csv')
    pyplot.savefig('google.csv.png', bbox_inches='tight')

def read__csvs(foldername):
    for filename in get_csv_files(foldername):
        _, site_name = os.path.split(filename)
        pyplot.figure()
        print 'File being processed: ' + filename 
        table = read_csv(filename)
        size_of_node = table[table['object'] == 'Node'].iloc[0]["size"]
        normalized_total_memory_used(group_timestamps(parse_object_destuction(table), 1000), size_of_node).order(ascending='true').plot(kind='bar')
        pyplot.xlabel('Objects')
        pyplot.ylabel('Memory in bytes')
        pyplot.title('Graph of objects vs memory for '+site_name)
        pyplot.savefig(site_name+'.png', bbox_inches='tight')

def plot_all_data(foldername, savedfig_name):
    total_memory_used_per_site = {}
    for filename in get_csv_files(foldername):
        _, site_name = os.path.split(filename)
        table = read_csv(filename)
        size_of_node = table[table['object'] == 'Node'].iloc[0]["size"]
        total_memory_used_per_site[site_name] = normalized_total_memory_used(group_timestamps(parse_object_destuction(table), 1000), size_of_node)

    total_memory_used_per_site = pandas.DataFrame(total_memory_used_per_site).transpose()
    total_memory_used_per_site.plot(kind='bar', stacked=True, colormap='hsv')

    pyplot.xlabel('Site name')
    pyplot.ylabel('Memory in bytes')
    pyplot.title('Stacked Graph of memory consumed by different sites')
    pyplot.savefig(savedfig_name, bbox_inches='tight')

def main():
    # Plots the graph of object against memory used for one site
    TEST_FILE = '/usr/local/google/Work/clockwork_csv/google.csv'
    read_individual_csv(TEST_FILE)

    # Plots the graph of object against memory used for all csvs found in a folder
    TEST_FOLDER = '/usr/local/google/Work/clockwork_csv'
    read__csvs(TEST_FOLDER)

    # Plots the stacked graph of memory taken up by objects across all sites. 
    plot_all_data(TEST_FOLDER, 'top_25.png')

if __name__ == "__main__":
    main()