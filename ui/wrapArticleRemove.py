#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2021 WShuai, Inc.
# All Rights Reserved.

# @File: wrapArticleRemove.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2021/1/20 15:12

import json
from PyQt5 import (
    QtGui,
    QtCore,
    QtWidgets
)

from .ui_dialog_article_remove import Ui_DialogArticleRemove

class WrapArticleRemove(QtWidgets.QDialog, Ui_DialogArticleRemove):
    signal_article = QtCore.pyqtSignal(str)

    def __init__(self, parent = None, configs = None):
        super(WrapArticleRemove, self).__init__(parent)
        self.setupUi(self)

        self.push_button_ok.clicked.connect(self.click_ok)
        self.push_button_cancel.clicked.connect(self.click_cancel)
        return

    def slot_remove(self, result):
        article = json.loads(result)
        self.line_edit_article_id.setText(article['id'])
        self.spin_box_article_num.setValue(article['num'])
        self.line_edit_article_time.setText(article['time'])
        self.line_edit_article_name.setText(article['name'])
        return

    def click_ok(self):
        self.signal_article.emit(None)
        self.close()
        return

    def click_cancel(self):
        self.close()
        return

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.line_edit_article_name.setText(None)
        self.line_edit_article_id.setText(None)
        self.spin_box_article_num.setValue(1)
        self.line_edit_article_time.setText(None)
        return