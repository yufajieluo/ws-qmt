#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2021 WShuai, Inc.
# All Rights Reserved.

# @File: wrapCelebrate.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2021/1/27 15:37

from PyQt5 import (
    QtGui,
    QtCore,
    QtWidgets,
    QtMultimedia
)

from .ui_dialog_celebrate import Ui_DialogCelebrate

class WrapCelebrate(QtWidgets.QDialog, Ui_DialogCelebrate):
    def __init__(self, parent = None, configs = None):
        super(WrapCelebrate, self).__init__(parent)
        self.setupUi(self)

        self.configs = configs

        self.move_celebrate = QtGui.QMovie(self.configs['celebrating_image_file'])
        self.move_celebrate.setScaledSize(self.label_celebrate.size())

        self.playlist = QtMultimedia.QMediaPlaylist()
        self.playlist.addMedia(
            QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(self.configs['celebrating_sound_file']))
        )
        self.playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)

        self.sound_celebrate = QtMultimedia.QMediaPlayer()
        self.sound_celebrate.setPlaylist(self.playlist)
        self.sound_celebrate.setVolume(100)
        return

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.label_celebrate.setMovie(self.move_celebrate)
        self.move_celebrate.start()
        self.sound_celebrate.play()
        return

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.move_celebrate.stop()
        self.sound_celebrate.stop()
        return