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
from subprocess import call

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
    COMPUTED_STYLE_PY = "/usr/local/google/home/nmduc/chromium-group-opt/src/third_party/WebKit/Source/build/scripts/make_computed_style_base.py"
    # COMPUTED_STYLE_PY = "./make_computed_style_base_test.py"
    # read computed style python
    code = ""
    with open(COMPUTED_STYLE_PY, "r") as fo:
        code = fo.read()

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

    # old_folder = os.getcwd()
    # for chromium_version_path in chromium_version_list.values():
    #     os.chdir(chromium_version_path)
    #     run_cmd("Build chromium: ", ["ninja", "-C", "out/Default", "-j", "1000", "blink_tests"])
    #     os.chdir(old_folder)

    # os.chdir(old_folder)

    result_memory = {}
    build_dir = "/usr/local/google/home/nmduc/chromium-group-opt/src/out"
    build_version_dirs = [i for i in os.listdir(build_dir) if "Default_" in i]
    for bdir in build_version_dirs:
        print bdir
        exec_dir = build_dir + "/" + bdir + "/content_shell"
        for website in website_list:
            now = time.time()
            try:
                summary = tryChromeWithWebsite(bdir, exec_dir, website, website_list[website])
            except:
                continue;
            result_memory[website, bdir, now] = summary
        saveToPickle(result_memory, "mini_benchmark_param" + time.strftime("%d_%m_%Y_%H_%M_%S", time.localtime()) + ".pkl")

    saveToPickle(result_memory, "mini_benchmark_param" + time.strftime("%d_%m_%Y_%H_%M_%S", time.localtime()) + ".pkl")
                # print("[" + str(i) + "," + str(j) + "," + str(k) + "]")
    #             for website in website_list:
    #                 now = time.time()
    #                 for chromium_version in chromium_version_list:
    #                     summary = tryChromeWithWebsite(chromium_version, chromium_version_list[chromium_version] + "/out/Default/content_shell",
    #                                          website, website_list[website])
    #                     result_memory[website, chromium_version + "[" + str(i) + "," + str(j) + "," + str(k) + "]", now] = summary
    # with open(COMPUTED_STYLE_PY, "w") as fw:
    #     fw.write(code)
    # saveToPickle(result_memory, "mini_benchmark_" + time.strftime("%d_%m_%Y_%H_%M_%S", time.localtime()) + ".pkl")



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
