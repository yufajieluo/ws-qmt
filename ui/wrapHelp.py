#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2021 WShuai, Inc.
# All Rights Reserved.

# @File: wrapHelp.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2021/1/28 15:04

from PyQt5 import QtWidgets

from .ui_dialog_help import Ui_DialogHelp

class WrapHelp(QtWidgets.QDialog, Ui_DialogHelp):
    def __init__(self, parent = None, configs = None, ):
        super(WrapHelp, self).__init__(parent)
        self.setupUi(self)

        self.configs = configs

        self.label_top.setText(self.configs['top'])
        self.label_left.setText(self.configs['left'])
        self.label_right.setText(self.configs['right'])

        return