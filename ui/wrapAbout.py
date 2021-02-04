#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2021 WShuai, Inc.
# All Rights Reserved.

# @File: wrapAbout.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2021/1/18 17:44

from PyQt5 import QtWidgets

from .ui_dialog_about import Ui_DialogAbout

class WrapAbout(QtWidgets.QDialog, Ui_DialogAbout):
    def __init__(self, parent = None, configs = None, ):
        super(WrapAbout, self).__init__(parent)
        self.setupUi(self)

        self.configs = configs

        self.label_title.setText(self.configs['service'])
        self.label_version.setText(self.configs['version'])
        self.label_explanation.setText(self.configs['explanation'])
        self.label_copyright.setText(self.configs['copyright'])

        return