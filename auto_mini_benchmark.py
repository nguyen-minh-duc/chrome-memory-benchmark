import os
import sys
import subprocess as sp
import time
import re
import Graphs
import json
import pandas

CHROMIUM_DIR = "~/chromium/src"
WEBSITE_LIST_FILE = "./website.txt"


def run_cmd(description, cmd):
    print '[{}] {}'.format(description, ' '.join(cmd))
    print cmd
    output = sp.call(cmd)
    return output

if __name__ == "__main__":
    CHROMIUM_DIR = sys.argv[1]
    WEBSITE_LIST_FILE = sys.argv[2]
    assert CHROMIUM_DIR[-3:] == "src", "Must be in src"
    # collect website url
    website_list = []
    with open(WEBSITE_LIST_FILE, "r") as fo:
        website_list = fo.readlines()

    website_list = [w.strip() for w in website_list]
    # build chromium at CHROMIUM_DIR
    old_folder = os.getcwd()
    print old_folder
    os.chdir(CHROMIUM_DIR)
    run_cmd("Build chromium: ", ["ninja", "-C", "out/Default", "-j", "1000", "chrome"])
    os.chdir(old_folder)
    # run website
    result_memory = {}
    for i in range(len(website_list)):
        out_log_file = "./" + "_".join(re.split("[^a-z]", website_list[i])) + "_group_opt" + ".csv"
        print [CHROMIUM_DIR + "/out/Default/chrome", website_list[i], ">", out_log_file]
        with open(out_log_file, "w") as fw:
            chrome_sp = sp.Popen([CHROMIUM_DIR + "/out/Default/chrome", website_list[i]], stdout=fw)
            time.sleep(25)
            chrome_sp.terminate()
            fw.close()
            time.sleep(5)
            result_memory[out_log_file] = Graphs.read_individual_csv(out_log_file, out_log_file + ".png")

    print json.dumps(result_memory.__dict__)

