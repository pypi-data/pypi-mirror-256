#!/usr/bin/env python3
# coding:utf-8
# @author: Peixuan Shu
# @date: 2024-2-12
# @brief: create .desktop file
# @license: BSD v3

import os

folder = os.path.dirname(os.path.abspath(__file__)) # absolute path of this folder 

text = '\
[Desktop Entry]\n\
Encoding=UTF-8\n\
Name=brightness-ui\n\
Comment=brightness-ui\n\
Exec={}/brightness-ui.sh\n\
Icon={}/image/logo.png\n\
Terminal=false\n\
Type=Application\n\
Categories=Application'.format(folder, os.path.dirname(folder))

def CreateDesktop():
    with open(folder+'/brightness-ui.desktop', 'w') as file:
        file.write(text)

if __name__ == '__main__':
    CreateDesktop()
