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
    print os.getcwd()
    # build with dif config
    for i in np.arange(0.2, 0.3, 0.1):
        for j in np.arange(0.3, 0.7, 0.1):
            for k in np.arange(0.1, 0.6, 0.1):
                code_new = code.replace("[0.1, 0.3, 1.0]", "[" + str(i) + ", " + str(j) +", 1.0]")
                code_new = code_new.replace("[0.1, 1.0]", "[" + str(k) +", 1.0]")
                with open(COMPUTED_STYLE_PY, "w") as fw:
                    fw.write(code_new)
                old_folder = os.getcwd()
                for chromium_version_path in chromium_version_list.values():
                    os.chdir(chromium_version_path)
                    build_folder = "out/Default_" + str(i) + "_" + str(j) + "_" + str(k)
                    # run_cmd("Gen build files: ", ["gn", "gen", "--args=use_goma=true", build_folder])
                    # run_cmd("Config: ", ["echo", "use_goma=true > " + build_folder + "/args.gn"])
                    # run_cmd("Gen build files: ", ["gn", "gen", build_folder])
                    run_cmd("Build chromium: ", ["ninja", "-C", "out/Default", "-j", "1000", "blink_tests"])
                    run_cmd("Copying build: ", ["cp", "-a", "out/Default", build_folder])
                    run_cmd("Copying make_computed_style_base: ", ["cp", COMPUTED_STYLE_PY, build_folder + "/"])
                    os.chdir(old_folder)
                os.chdir(old_folder)
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
