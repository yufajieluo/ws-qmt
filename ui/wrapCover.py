#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2021 WShuai, Inc.
# All Rights Reserved.

# @File: wrapCover.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2021/1/19 15:48

from PyQt5 import (
    QtGui,
    QtCore,
    QtWidgets
)

from .ui_window_cover import Ui_MainWindow
from .wrapAbout import WrapAbout
from .wrapHelp import WrapHelp
from .wrapMain import WrapMain

class WrapCover(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None, configs = None, handlers = None):
        super(WrapCover, self).__init__(parent)
        self.setupUi(self)
        self.show()

        self.configs = configs
        self.handlers = handlers

        self.label_help.click.connect(self.click_help)
        self.label_start.click.connect(self.click_start)
        self.label_about.click.connect(self.click_about)

        self.dialog_about = WrapAbout(configs = self.configs['about'])
        self.dialog_help = WrapHelp(configs = self.configs['help'])
        self.window_main = WrapMain(configs = self.configs['main'], handlers = self.handlers)

        self.window_main.signal_close.connect(self.reshow)
        return

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.window_main.thread_init.quit()
        self.window_main.thread_init.wait()
        return

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        print('鼠标进入')
        self.label_help.setCursor(QtCore.Qt.OpenHandCursor)
        self.label_about.setCursor(QtCore.Qt.OpenHandCursor)
        self.label_start.setCursor(QtCore.Qt.OpenHandCursor)
        return

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        print('鼠标离开')
        return

    def click_help(self):
        return

    def click_start(self):
        self.setVisible(False)
        self.window_main.show()
        # 子界面关闭时，主界面要显示出来 reshow
        return

    def click_about(self):
        self.dialog_about.setWindowModality(QtCore.Qt.ApplicationModal)
        self.dialog_about.show()
        return

    def click_help(self):
        self.dialog_help.show()
        return

    def reshow(self):
        self.setVisible(True)