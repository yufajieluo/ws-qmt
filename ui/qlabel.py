#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2021 WShuai, Inc.
# All Rights Reserved.

# @File: qlabel.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2021/1/18 15:51

from PyQt5 import (
    QtWidgets,
    QtCore,
    QtGui
)

class QLabel(QtWidgets.QLabel):
    click = QtCore.pyqtSignal()

    def __init__(self, parent = None):
        super(QLabel, self).__init__(parent)
        return

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.setCursor(QtCore.Qt.ClosedHandCursor)
        return

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.setCursor(QtCore.Qt.OpenHandCursor)

        if ev.button() == QtCore.Qt.LeftButton:
            self.click.emit()
        return