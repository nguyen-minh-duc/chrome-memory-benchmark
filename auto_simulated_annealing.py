import os
import sys
import subprocess as sp
import time
import re
import Graphs
import json
import pandas
import json
import pickle as pkl
import numpy as np
import scipy.optimize as optimizet

def run_cmd(description, cmd):
    print '[{}] {}'.format(description, ' '.join(cmd))
    print cmd
    output = sp.call(cmd)
    return output


def splitIgnoreConsecutiveDelim(string, delim):
    return re.split(string, "[" + delim + "]+")


def saveToPickle(object_, filename):
    with open(filename, "w") as fw:
        pkl.dump(object_, fw, pkl.HIGHEST_PROTOCOL)


def tryChromeWithWebsite(chrome_name, chrome, website_name, website):
    """Run chrome with website

    Args:
        chrome: path to chrome binary. Ex: out/Default/chrome
        website: website url

    Returns:
        Summary of object created and their normalized size
    """
    out_log_file = "./" + website_name + "_" + chrome_name + ".csv"
    print out_log_file
    with open(out_log_file, "w") as fwrite:
        chrome_sp = sp.Popen([chrome, website], stdout=fwrite, preexec_fn=os.setsid)
        time.sleep(25)
        try:
            # os.killpg(os.getpgid(chrome_sp.pid), signal.SIGTERM)
            chrome_sp.terminate()
            # chrome_sp.send_signal(-9)
        except OSError:

            # can't kill a dead proc
            pass
        print chrome_sp.wait()
        # fwrite.close()
    return Graphs.read_individual_csv(out_log_file, out_log_file + ".png")


def main():
    WEBSITE_LIST_FILE = "./website.txt"
    CHROMIUM_VERSION_FILES = "./chromium.txt"
    CHROMIUM_VERSION_FILES = sys.argv[1]
    WEBSITE_LIST_FILE = sys.argv[2]
    # collect website url
    website_list = []

    with open(WEBSITE_LIST_FILE, "r") as fo:
        website_list = json.load(fo)
        fo.close()

    # collect chromium version
    chromium_version_list = []
    with open(CHROMIUM_VERSION_FILES, "r") as fo:
        chromium_version_list = json.load(fo)
        fo.close()

    old_folder = os.getcwd()
    for chromium_version_path in chromium_version_list.values():
        os.chdir(chromium_version_path)
        run_cmd("Build chromium: ", ["ninja", "-C", "out/Default", "-j", "1000", "chrome"])
        os.chdir(old_folder)

    os.chdir(old_folder)


    #
    # # build chromium at CHROMIUM_DIR
    # old_folder = os.getcwd()
    # print old_folder
    # os.chdir(CHROMIUM_DIR)
    # run_cmd("Build chromium: ", ["ninja", "-C", "out/Default", "-j", "1000", "chrome"])
    # os.chdir(old_folder)
    # # run website
    # result_memory = {}
    # for i in range(len(website_list)):
    #     out_log_file = "./" + "_".join(re.split("[^a-z]", website_list[i])) + "_group_opt" + ".csv"
    #     print [CHROMIUM_DIR + "/out/Default/chrome", website_list[i], ">", out_log_file]
    #     with open(out_log_file, "w") as fw:
    #         chrome_sp = sp.Popen([CHROMIUM_DIR + "/out/Default/chrome", website_list[i]], stdout=fw)
    #         time.sleep(25)
    #         chrome_sp.terminate()
    #         fw.close()
    #         time.sleep(5)
    #         result_memory[out_log_file] = Graphs.read_individual_csv(out_log_file, out_log_file + ".png")

    # print json.dumps(result_memory.__dict__)

if __name__ == "__main__":
    main()
