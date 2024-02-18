#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# install dependencies
sudo apt install python3-pip
pip3 install PyQt5

# install brightness-ui package
pip3 install -e .

# install desktop shortcut
cd brightnessUI/install/
python3 create_desktop.py # create brightness-ui.desktop
cp brightness-ui.desktop ~/Desktop/brightness-ui.desktop
sudo cp brightness-ui.desktop /usr/share/applications/brightness-ui.desktop
