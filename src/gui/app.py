import sys
import os

from dandere2x import Dandere2x
from dandere2x_core.dandere2x_utils import get_valid_block_sizes
from wrappers.videosettings import VideoSettings
import subprocess

from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QWidget, QFileDialog
from Dandere2xGUI import Ui_Dandere2xGUI
from PyQt5 import QtCore, QtGui, QtWidgets



class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dandere2xGUI()
        self.ui.setupUi(self)

        self.file_dir = ''
        self.workspace_dir = ''

        #self.ui.video_icon.setPixmap(QtGui.QPixmap("assets\\aka.png"))

        self.config_buttons()
        self.show()

    def config_buttons(self):
        self.ui.select_video_button.clicked.connect(self.press_select_video_button)
        self.ui.select_workspace_button.clicked.connect(self.press_select_workspace_button)
        self.ui.upscale_button.clicked.connect(self.press_upscale_button)

    def press_upscale_button(self):
        d = Dandere2x('C:\\Users\\windwoz\\Documents\\github_projects\\src\\config.ini')

        print(self.file_dir)

        self.workspace_dir = self.workspace_dir.replace("/","\\")
        self.file_dir = self.file_dir.replace("/","\\")

        print("workspace = " + self.workspace_dir)
        print("file_dir = " + self.file_dir)

        # d.context.file_dir = self.file_dir
        # d.context.workspace = self.workspace_dir
        self.ui.upscale_status.setText("Upscaling in Progress")
        d.run_concurrent()

    def press_select_video_button(self):

        self.file_dir = self.load_file()[0]

        path, name = os.path.split(self.file_dir)

        self.ui.video_label.setText(name)
        self.ui.video_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))

        valid_list = get_valid_block_sizes(1920,1080)
        self.ui.block_size_combo_box.addItems(valid_list)
        self.ui.block_size_combo_box.setEnabled(True)


    def press_select_workspace_button(self):

        self.workspace_dir = self.load_dir()

        start_val = len(self.workspace_dir) - 20
        if(start_val < 0):
            start_val = 0

        self.ui.workspace_label.setText(".." + self.workspace_dir[start_val :  len(self.workspace_dir)])
        self.ui.workspace_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))

        print( self.workspace_dir )


    def load_dir(self):
        self.ui.w = QWidget()

        # Set window size.
        self.ui.w.resize(320, 240)
        filename = QFileDialog.getExistingDirectory(w, 'Open Directory', 'C:\\Users\\windwoz\\Desktop\\plz\\pythonreleases\\1.1\\demo_folder\\')
        return filename

    def load_file(self):
        self.ui.w = QWidget()

        # Set window size.
        self.ui.w.resize(320, 240)
        filename = QFileDialog.getOpenFileName(w, 'Open File', 'C:\\Users\\windwoz\\Desktop\\plz\\pythonreleases\\1.1\\demo_folder\\')
        return filename

app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())