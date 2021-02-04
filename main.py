#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2021 WShuai, Inc.
# All Rights Reserved.

# @File: main.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2021/1/16 15:45

import os
import sys
#sys.path.append(os.path.dirname(__file__) + os.sep + '../')
import PyQt5.sip
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('auto')

from common import (
    commLog,
    commFile
)
from ui import wrapCover
from service import jdSeckill

if __name__ == '__main__':
    config_file = 'config/config.yaml'

    # init config
    file_handler = commFile.FileHandler()
    configs = file_handler.loads(file = config_file, type = 'yaml')
    print('read config is {0}'.format(configs))

    # init log
    log_handler = commLog.LogHandler(configs['logging'])
    log_path = os.path.dirname(configs['logging']['handlers']['default']['filename'])
    if not os.path.isdir(log_path):
        os.makedirs(log_path)
    logger = log_handler.register_rotate(configs['application']['about']['service'].lower())
    logger.info('service config is {}'.format(configs))

    # init Seckill
    configs['seckill']['logging'] = configs['logging']
    jd_seckill = jdSeckill.JdSeckill(configs['seckill'], logger = logger)

    # init app
    handlers = {
        'file_handler': file_handler,
        'seckill_handler': jd_seckill
    }

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    #QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = wrapCover.WrapCover(configs = configs['application'], handlers = handlers)
    window.show()
    app.exec_()

    sys.exit(0)