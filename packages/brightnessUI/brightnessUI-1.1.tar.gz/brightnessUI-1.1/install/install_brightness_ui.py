#!/usr/bin/env python3
# coding:utf-8
# @author: Peixuan Shu
# @date: 2024-2-15
# @brief: Install brightness ui
# @license: BSD v3

import os
import subprocess
from .create_desktop import CreateDesktop

folder = os.path.dirname(os.path.abspath(__file__)) # absolute path of this folder 

def main():
    # print("install folder: " + folder)
    ### Create brightness-ui.desktop
    CreateDesktop()
    ### Create Desktop shortcut
    subprocess.run("cp {}/brightness-ui.desktop ~/Desktop/brightness-ui.desktop".format(folder), shell=True)
    ### Create Application Menu shortcut
    subprocess.run("sudo cp {}/brightness-ui.desktop /usr/share/applications/brightness-ui.desktop".format(folder), shell=True)
    print("Finish creating desktop and application menu shorcuts.")

if __name__ == '__main__':
    main()