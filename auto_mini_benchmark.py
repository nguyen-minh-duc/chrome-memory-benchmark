import os
import sys
import subprocess as sp
import time
import re
import Graphs
import json
import pandas
import pickle as pkl

CHROMIUM_DIR = "~/chromium/src"
WEBSITE_LIST_FILE = "./website.txt"


def run_cmd(description, cmd):
    print '[{}] {}'.format(description, ' '.join(cmd))
    print cmd
    output = sp.call(cmd)
    return output

def saveToPickle(object_, filename):
    with open(filename, "w") as fw:
        pkl.dump(object_, fw, pkl.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    CHROMIUM_DIR = sys.argv[1]
    WEBSITE_LIST_FILE = sys.argv[2]
    assert CHROMIUM_DIR[-3:] == "src", "Must be in src"
    # collect website url
    website_list = []

    with open(WEBSITE_LIST_FILE, "r") as fo:
        website_list = json.load(fo)
        fo.close()

    # build chromium at CHROMIUM_DIR
    old_folder = os.getcwd()
    print old_folder
    os.chdir(CHROMIUM_DIR)
    run_cmd("Build chromium: ", ["ninja", "-C", "out/Default", "-j", "1000", "blink_tests"])
    os.chdir(old_folder)
    # run website
    result_memory = {}
    for website in website_list:
        now = time.time()
        out_log_file = "./" + website + "_up_opt" + ".csv"
        print [CHROMIUM_DIR + "/out/Default/content_shell", website_list[website], ">", out_log_file]
        with open(out_log_file, "w") as fw:
            chrome_sp = sp.Popen([CHROMIUM_DIR + "/out/Default/content_shell", website_list[website]], stdout=fw)
            time.sleep(25)
            chrome_sp.terminate()
            fw.close()
        result_memory[website, "task_1_group_opt", now] = Graphs.read_individual_csv(out_log_file, out_log_file + ".png")
    saveToPickle(result_memory, "task1_group_opt_benchmark" + time.strftime("%d_%m_%Y_%H_%M_%S", time.localtime()) + ".pkl")



