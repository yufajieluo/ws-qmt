#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2021 WShuai, Inc.
# All Rights Reserved.

# @File: wrapArticleModify.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2021/1/20 13:55

import json
from PyQt5 import (
    QtGui,
    QtCore,
    QtWidgets
)

from .ui_dialog_article_modify import Ui_DialogArticleModify

class WrapArticleModify(QtWidgets.QDialog, Ui_DialogArticleModify):
    signal_article = QtCore.pyqtSignal(str)

    def __init__(self, parent = None, configs = None):
        super(WrapArticleModify, self).__init__(parent)
        self.setupUi(self)

        self.push_button_ok.clicked.connect(self.click_ok)
        self.push_button_cancel.clicked.connect(self.click_cancel)
        return

    def slot_modify(self, result):
        article = json.loads(result)
        #print('article is {}'.format(article))
        self.line_edit_article_id.setText(article['id'])
        self.spin_box_article_num.setValue(article['num'])
        self.line_edit_article_time.setText(article['time'])
        self.line_edit_article_name.setText(article['name'])
        #print('----')
        return

    def click_ok(self):
        if not self.line_edit_article_name.text() or not self.line_edit_article_id.text() or not self.line_edit_article_time.text():
            QtWidgets.QMessageBox.warning(self, '警告', '请完整填写商品信息')
        else:
            article_info = {
                'name': self.line_edit_article_name.text(),
                'id': self.line_edit_article_id.text(),
                'num': self.spin_box_article_num.value(),
                'time': self.line_edit_article_time.text()
            }
            self.signal_article.emit(json.dumps(article_info))
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