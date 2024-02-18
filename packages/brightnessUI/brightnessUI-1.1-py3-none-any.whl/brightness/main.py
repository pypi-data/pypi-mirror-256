#!/usr/bin/env python3
# coding:utf-8
# @author: Peixuan Shu
# @date: 2024-2-8
# @brief: Change screen backlight by modifying /sys/class/backlight/xxx/brightness
# @license: BSD v3

import sys
import os
import signal
import subprocess
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import*
from PyQt5.QtCore import *
from PyQt5.QtGui import QCloseEvent, QIcon, QPixmap
from PyQt5.QtWidgets import QWidget
from .ui.main_window import *
from .ui.password import *
from .ui.backlight_slider import *

class PasswordWin(QWidget, Ui_PassWord):
    """ Password widget """
    confirm_signal = pyqtSignal(bool, str)
    close_signal = pyqtSignal()
    def __init__(self):
        super(PasswordWin, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("password")
        # self.resize(280,100)
        self.password_lineEdit.returnPressed.connect(self.confirm) # 'Enter' callback

    def confirm(self):
        pwd = self.password_lineEdit.text()
        self.confirm_signal.emit(True, pwd)
        self.close()

    def closeEvent(self, event):
        self.close_signal.emit()
        print("close password window")
        return super().closeEvent(event)

class BackLightSlider(QWidget, Ui_BackLightSlider):
    """ Back light slider widget """
    debug_mesg_signal = pyqtSignal(str)
    sync_password_signal = pyqtSignal(str)
    def __init__(self, folder):
        super(BackLightSlider, self).__init__()
        self.setupUi(self)
        # self.resize(280,100)
        self.folder = folder
        self.folder_label.setText("   {}".format(folder))
        ### Set slider initial value
        get_value = subprocess.getoutput("cat /sys/class/backlight/{}/brightness".format(folder))
        self.horizontalSlider.setValue(int(get_value))
        self.value_label.setText(get_value)
        ### Connect to slider signals
        self.horizontalSlider.valueChanged.connect(self.tune_backlight)
        # self.horizontalSlider.sliderReleased.connect(self.tune_backlight)

        self.password = None

    def tune_backlight(self, value):
        ### Clear debug messages
        self.debug_mesg_signal.emit('')

        ### Read password
        if self.password is None:
            self.password_win = PasswordWin()
            self.password_win.confirm_signal.connect(self.set_password)
            self.password_win.close_signal.connect(self.resume_value)
            self.password_win.show()
        else:
            self.set_backlight()

        # ### Read password
        # if self.password is None:
        #     password, ok = QInputDialog.getText(self, 'Password', "sudo password: ")
        #     if ok:
        #         self.password = password
        #     else:
        #         print("Password Input Cancled")

    def set_password(self, ok, pwd):
        if ok:
            self.password = pwd
            self.sync_password_signal.emit(pwd) # update password for other sliders
            self.set_backlight()
        else:
            self.password = None    

    def set_backlight(self):
        value = self.horizontalSlider.value()
        ### Set backlight
        if self.password != None:
            # set_value = subprocess.getoutput("echo {} | sudo tee /sys/class/backlight/nvidia_0/brightness".format(value))
            # set_value = subprocess.getoutput("sudo sh -c \"echo {} > /sys/class/backlight/nvidia_0/brightness\" ".format(value))
            set_text = subprocess.getoutput("echo {} | sudo -S sh -c \"echo {} > /sys/class/backlight/{}/brightness\" ".format(self.password, value, self.folder))
            self.debug_mesg_signal.emit(set_text)
            if 'incorrect password' in set_text:
                self.password = None
        ### Resume slider and label
        self.resume_value()
        print("set {} backlight value: {}".format(self.folder, value))
    
    def resume_value(self):
        get_value = subprocess.getoutput("cat /sys/class/backlight/{}/brightness".format(self.folder))
        self.value_label.setText(get_value)
        # self.horizontalSlider.setValue(int(get_value)) # will trigger tune_backlight (not expected)
        

class MainWindow(QMainWindow,Ui_MainWindow):
    """ Main window """
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.password = None

        ### Inquiry backlight folders
        path = '/sys/class/backlight/'
        backlight_folders = []
        for item in os.listdir(path):
            if os.path.isdir(path+item):
                backlight_folders.append(item)
                print("find {} in /sys/class/backlight/".format(item))
            else:
                print("{} is not a directory".format(item))
        # print("backlights in /sys/class/backlight: {}".format(backlight_folders))

        ### Add BackLightSlider for each backlight folder
        self.backlight_sliders = []
        self.slider_verticalLayout = QVBoxLayout(self.sliders_widget)
        for folder in backlight_folders:
            backlight_slider = BackLightSlider(folder)
            backlight_slider.debug_mesg_signal.connect(self.set_debug_mesg)
            backlight_slider.sync_password_signal.connect(self.sync_password)
            self.backlight_sliders.append(backlight_slider)
            self.slider_verticalLayout.addWidget(backlight_slider) # Add widgets dynamically
        # self.sliders_widget.resize(self.slider_verticalLayout.sizeHint())
        
        ### resize after adding widgets
        self.resize(self.verticalLayout.sizeHint())
    
    def set_debug_mesg(self, mesg):
        self.mesg_label.setText(mesg)
    
    def sync_password(self, pwd):
        for slider in self.backlight_sliders:
            slider.password = pwd

class MainUI(QObject):
    def __init__(self):
        super(MainUI,self).__init__()
        self.run()

    def run(self):
        ### Create QApplication window
        self.app = QApplication(sys.argv)

        ### Create Main window
        w = MainWindow()
        # w.resize(400, 200)
        # w.move(300, 300)
        w.setWindowTitle("Brightness")
        ## Set logo icon
        workspace = os.path.dirname(os.path.abspath(__file__)) # absolute path of this folder 
        icon = QIcon() # 地面站logo
        # print(workspace)
        icon.addPixmap(QPixmap(workspace+"/image/logo.png"), QIcon.Normal, QIcon.Off)
        w.setWindowIcon(icon)
        w.show()
        print("Brightness UI")

        # Block the main funcaton. Release resourses.
        signal.signal(signal.SIGINT, self._signal_handler) # catch Ctrl+C or terminate()
        sys.exit(self.app.exec_())
    
    def _signal_handler(self, signal, frame):
        sys.exit(0)

def main():
    """ Entry points for brightness-ui command """
    MainUI()

if __name__ == '__main__':
    main()
