#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2021 WShuai, Inc.
# All Rights Reserved.

# @File: main.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2021/1/16 15:45

import os
import time
import json
from PyQt5 import (
    QtGui,
    QtCore,
    QtWidgets
)

from .ui_window_main import Ui_MainWindow
from .wrapCelebrate import WrapCelebrate
from .wrapArticleAdd import WrapArticleAdd
from .wrapArticleModify import WrapArticleModify
from .wrapArticleRemove import WrapArticleRemove


from .backend import (
    Init,
    QrCode,
    Reserve,
    Seckill
)

class WrapMain(QtWidgets.QMainWindow, Ui_MainWindow):
    signal_load_login = QtCore.pyqtSignal()
    signal_article_modify = QtCore.pyqtSignal(str)
    signal_close = QtCore.pyqtSignal()

    def __init__(self, parent = None, configs = None, handlers = None):
        super(WrapMain, self).__init__(parent)
        self.setupUi(self)

        self.eid_fp = None
        self.active_article = None
        self.status = 'init'

        self.configs = configs
        self.handlers = handlers

        self.move_qrcode = QtGui.QMovie(configs['qrcoding_image_file'])
        self.move_qrcode.setScaledSize(self.label_qrcode.size())

        self.move_reserve = QtGui.QMovie(configs['reserving_image_file'])
        self.move_reserve.setScaledSize(self.label_qrcode.size())

        self.move_seckill = QtGui.QMovie(configs['seckilling_image_file'])
        self.move_seckill.setScaledSize(self.label_seckill.size())

        self.loads_article()
        self.table_widget_article.setHorizontalHeaderLabels([item['value'] for item in self.configs['article']['title']])

        self.dialog_celebrate = WrapCelebrate(configs = self.configs)
        self.dialog_article_add = WrapArticleAdd()
        self.dialog_article_modify = WrapArticleModify()
        self.dialog_article_remove = WrapArticleRemove()

        self.signal_article_modify.connect(self.dialog_article_modify.slot_modify)
        self.signal_article_modify.connect(self.dialog_article_remove.slot_remove)

        self.push_button_add.clicked.connect(self.click_add)
        self.dialog_article_add.signal_article.connect(self.slot_add)

        self.push_button_modify.clicked.connect(self.click_modify)
        self.dialog_article_modify.signal_article.connect(self.slot_modify)

        self.push_button_remove.clicked.connect(self.click_remove)
        self.dialog_article_remove.signal_article.connect(self.slot_remove)

        self.push_button_active.clicked.connect(self.click_active)

        self.push_button_getqr.clicked.connect(self.click_getqr)
        self.thread_qrcode = QrCode(handlers = self.handlers)
        self.thread_qrcode.signal_qrcode.connect(self.slot_getqr)
        self.thread_qrcode.signal_login.connect(self.slot_login)

        self.push_button_reserve.clicked.connect(self.click_reserve)
        self.thread_reserve = Reserve(handlers = self.handlers)
        self.thread_reserve.signal_reserve.connect(self.slot_reserve)

        self.push_button_seckill.clicked.connect(self.click_seckill)
        self.thread_seckill = Seckill(handlers = self.handlers)
        self.thread_seckill.signal_sekill.connect(self.slot_seckill)

        self.push_button_stop.clicked.connect(self.click_stop)

        self.thread_init = Init(handlers = self.handlers)
        self.thread_init.signal_cookie.connect(self.slot_init)
        self.thread_init.signal_eidfp.connect(self.slot_eidfp)
        self.thread_init.start()



        if not os.path.isdir(self.configs['article']['path']):
            os.makedirs(self.configs['article']['path'])

        self.status_show()
        return



    def click_add(self):
        self.dialog_article_add.setWindowModality(QtCore.Qt.ApplicationModal)
        self.dialog_article_add.show()
        return

    def click_modify(self):
        if (self.table_widget_article.currentRow() < 0):
            QtWidgets.QMessageBox.warning(self, '警告', '请选择一个商品')
        else:
            article_info = {
                'id': self.table_widget_article.item(self.table_widget_article.currentRow(), 0).text(),
                'num': int(self.table_widget_article.item(self.table_widget_article.currentRow(), 1).text()),
                'time': self.table_widget_article.item(self.table_widget_article.currentRow(), 2).text(),
                'name': self.table_widget_article.item(self.table_widget_article.currentRow(), 3).text()
            }
            self.signal_article_modify.emit(json.dumps(article_info))

            self.dialog_article_modify.setWindowModality(QtCore.Qt.ApplicationModal)
            self.dialog_article_modify.show()
        return

    def click_remove(self):
        if (self.table_widget_article.currentRow() < 0):
            QtWidgets.QMessageBox.warning(self, '警告', '请选择一个商品')
        else:
            article_info = {
                'id': self.table_widget_article.item(self.table_widget_article.currentRow(), 0).text(),
                'num': int(self.table_widget_article.item(self.table_widget_article.currentRow(), 1).text()),
                'time': self.table_widget_article.item(self.table_widget_article.currentRow(), 2).text(),
                'name': self.table_widget_article.item(self.table_widget_article.currentRow(), 3).text()
            }
            self.signal_article_modify.emit(json.dumps(article_info))

            self.dialog_article_remove.setWindowModality(QtCore.Qt.ApplicationModal)
            self.dialog_article_remove.show()
        return

    def click_active(self):
        if(self.table_widget_article.currentRow() < 0):
            QtWidgets.QMessageBox.warning(self, '警告', '请选择一个商品')
        else:
            self.active_article = {
                'id': self.table_widget_article.item(self.table_widget_article.currentRow(), 0).text(),
                'num': int(self.table_widget_article.item(self.table_widget_article.currentRow(), 1).text()),
                'time': self.table_widget_article.item(self.table_widget_article.currentRow(), 2).text(),
                'name': self.table_widget_article.item(self.table_widget_article.currentRow(), 3).text()
            }
            article_items = []
            for item in self.configs['article']['title']:
                article_items.append('<font color=blue>{}: {}</font>'.format(item['value'], self.active_article[item['key']]))
            active_info = '<p>'.join(article_items)
            self.text_browser_active.setText(active_info)
        return

    def slot_add(self, result):
        #print('add result is {}'.format(json.loads(result)))
        article = json.loads(result)
        row = self.table_widget_article.rowCount()
        #print('row is {}'.format(row))
        self.table_widget_article.insertRow(row)

        self.table_widget_article.setItem(row, 0, QtWidgets.QTableWidgetItem(article['id']))
        self.table_widget_article.setItem(row, 1, QtWidgets.QTableWidgetItem(str(article['num'])))
        self.table_widget_article.setItem(row, 2, QtWidgets.QTableWidgetItem(article['time']))
        self.table_widget_article.setItem(row, 3, QtWidgets.QTableWidgetItem(article['name']))

        self.dumps_article()
        return

    def slot_modify(self, result):
        article = json.loads(result)
        #print('{}'.format(self.table_widget_article.currentRow()))
        #print('modify article is {}'.format(article))
        row = self.table_widget_article.currentRow()
        self.table_widget_article.setItem(row, 0, QtWidgets.QTableWidgetItem(article['id']))
        self.table_widget_article.setItem(row, 1, QtWidgets.QTableWidgetItem(str(article['num'])))
        self.table_widget_article.setItem(row, 2, QtWidgets.QTableWidgetItem(article['time']))
        self.table_widget_article.setItem(row, 3, QtWidgets.QTableWidgetItem(article['name']))

        self.dumps_article()
        return

    def slot_remove(self, result):
        self.table_widget_article.removeRow(self.table_widget_article.currentRow())

        self.dumps_article()
        return

    #==========================================#

    def click_getqr(self):
        self.thread_qrcode.start()
        self.status = 'qrcodeg'
        self.status_show(msg = '获取二维码中...')
        return

    def click_reserve(self):
        if not self.active_article:
            QtWidgets.QMessageBox.warning(self, '警告', '请激活一个商品')
        elif not self.handlers['seckill_handler'].qrlogin.is_login:
            QtWidgets.QMessageBox.warning(self, '警告', '请先登录')
        else:
            self.thread_reserve.set_article(self.active_article)
            self.thread_reserve.start()

            self.status = 'reserveg'
            self.status_show(msg='预约中...')
        return

    def click_seckill(self):
        if not self.active_article:
            QtWidgets.QMessageBox.warning(self, '警告', '请激活一个商品')
        elif not self.handlers['seckill_handler'].qrlogin.is_login:
            QtWidgets.QMessageBox.warning(self, '警告', '请先登录')
        elif not self.eid_fp:
            QtWidgets.QMessageBox.critical(self, '错误', '正在获取参数eid和fp，请稍等')
        else:
            self.thread_seckill.set_eid_fp(self.eid_fp)
            self.thread_seckill.set_article(self.active_article)
            self.thread_seckill.start()

            self.status = 'seckillsg'
            self.status_show(msg='抢购开始...')
        return

    def click_stop(self):
        self.thread_seckill.stop('manual')
        return

    def slot_init(self, result):
        result_json = json.loads(result)
        if result_json['ret']:
            self.status = 'logined'
            self.status_show(msg = 'cookie登录成功')
        return

    def slot_eidfp(self, result):
        self.eid_fp = json.loads(result)
        return

    def slot_login(self, result):
        result_json = json.loads(result)
        if result_json['ret']:
            self.status = 'logined'
        else:
            self.status = 'loginer'
        self.status_show(msg = result_json['msg'])
        return

    def slot_getqr(self, result):
        self.status = 'qrcoded'
        self.status_show(msg = '请扫描二维码登录', image = result)
        return

    def slot_reserve(self, result):
        result_json = json.loads(result)
        if result_json['ret']:
            self.status = 'reserved'
        else:
            self.status = 'reserver'
        self.status_show(msg = result_json['msg'])
        return

    def slot_seckill(self, result):
        result_json = json.loads(result)

        if result_json['type'] == 'success':
            self.status = 'seckilled'
            self.status_show(msg='抢购成功')
        else:
            self.status = 'seckillsp'
            self.status_show(msg='抢购已停止')
        return

    def dumps_article(self):
        articles = []
        for row in range(self.table_widget_article.rowCount()):
            article = {}
            for col in range(len(self.configs['article']['title'])):
                article[self.configs['article']['title'][col]['key']] = self.table_widget_article.item(row, col).text()
            articles.append(article)
        #print('articles is {}'.format(articles))

        self.handlers['file_handler'].dumps(
            content = articles,
            file = os.path.join(self.configs['article']['path'], self.configs['article']['file']),
            type = 'pickle')
        return

    def loads_article(self):
        articles = self.handlers['file_handler'].loads(
            file = os.path.join(self.configs['article']['path'], self.configs['article']['file']),
            type = 'pickle'
        )
        #print('articles is {}{}'.format(type(articles), articles))
        if articles:
            row = 0
            for article in articles:
                self.table_widget_article.insertRow(self.table_widget_article.rowCount())
                self.table_widget_article.setItem(row, 0, QtWidgets.QTableWidgetItem(article['id']))
                self.table_widget_article.setItem(row, 1, QtWidgets.QTableWidgetItem(str(article['num'])))
                self.table_widget_article.setItem(row, 2, QtWidgets.QTableWidgetItem(article['time']))
                self.table_widget_article.setItem(row, 3, QtWidgets.QTableWidgetItem(article['name']))
                row += 1
        return

    def status_show(self, msg = None, image = None):
        if self.status == 'init':
            self.label_qrcode.setPixmap(QtGui.QPixmap(self.configs['default_image_file']))
            self.label_seckill.setPixmap(QtGui.QPixmap(self.configs['default_image_file']))

            self.push_button_seckill.setEnabled(False)
            self.push_button_stop.setEnabled(False)

        elif self.status == 'qrcodeg':
            # 获取二维码中
            self.text_browser_login.append(
                '<font color={}>{} - {}</font>'.format(
                    'blue', time.strftime('%H:%M:%S'), msg
                )
            )
            self.text_browser_login.moveCursor(self.text_browser_seckill.textCursor().End)
            self.label_qrcode.setMovie(self.move_qrcode)
            self.move_qrcode.start()

            self.push_button_getqr.setEnabled(False)

        elif self.status == 'qrcoded':
            # 获取二维码成功
            self.text_browser_login.append(
                '<font color={}>{} - {}</font>'.format(
                    'blue', time.strftime('%H:%M:%S'), msg
                )
            )
            self.text_browser_login.moveCursor(self.text_browser_login.textCursor().End)
            self.move_qrcode.stop()
            self.label_qrcode.setPixmap(QtGui.QPixmap(image).scaled(158, 158))

            self.push_button_getqr.setEnabled(False)

        elif self.status == 'qrcoder':
            # 获取二维码失败
            pass

        elif self.status == 'logined':
            # 登录成功
            self.text_browser_login.append(
                '<font color={}>{} - {}</font>'.format(
                    'green', time.strftime('%H:%M:%S'), msg
                )
            )
            self.text_browser_login.append(
                '<font color={}>{} - 当前用户: {}</font>'.format(
                    'green', time.strftime('%H:%M:%S'), self.handlers['seckill_handler'].nick_name
                )
            )
            self.text_browser_login.moveCursor(self.text_browser_login.textCursor().End)
            self.label_qrcode.setPixmap(QtGui.QPixmap(self.configs['login_success_image_file']))

            self.push_button_getqr.setEnabled(True)

        elif self.status == 'loginer':
            # 登录失败
            self.text_browser_login.append(
                '<font color={}>{} - {}</font>'.format(
                    'red', time.strftime('%H:%M:%S'), msg
                )
            )
            self.text_browser_login.moveCursor(self.text_browser_login.textCursor().End)
            self.label_qrcode.setPixmap(QtGui.QPixmap(self.configs['login_failed_image_file']))

            self.push_button_getqr.setEnabled(True)

        elif self.status == 'reserveg':
            self.text_browser_seckill.append(
                '<font color={}>{} - {}</font>'.format(
                    'blue', time.strftime('%H:%M:%S'), msg
                )
            )
            self.text_browser_seckill.moveCursor(self.text_browser_seckill.textCursor().End)
            self.label_seckill.setMovie(self.move_reserve)
            self.move_reserve.start()

            self.push_button_reserve.setEnabled(False)
            self.push_button_seckill.setEnabled(False)

        elif self.status == 'reserved':
            # 预约成功
            self.text_browser_seckill.append(
                '<font color={}>{} - {}</font>'.format(
                    'green', time.strftime('%H:%M:%S'), msg
                )
            )
            self.text_browser_seckill.moveCursor(self.text_browser_seckill.textCursor().End)
            self.move_reserve.stop()
            self.label_seckill.setPixmap(QtGui.QPixmap(self.configs['reserve_success_iamge_file']))

            self.push_button_reserve.setEnabled(True)
            self.push_button_seckill.setEnabled(True)

        elif self.status == 'reserver':
            # 预约失败
            self.text_browser_seckill.append(
                '<font color={}>{} - {}</font>'.format(
                    'red', time.strftime('%H:%M:%S'), msg
                )
            )
            self.text_browser_seckill.moveCursor(self.text_browser_seckill.textCursor().End)
            self.move_reserve.stop()
            self.label_seckill.setPixmap(QtGui.QPixmap(self.configs['reserve_failed_iamge_file']))

            self.push_button_reserve.setEnabled(True)
            self.push_button_seckill.setEnabled(False)

        elif self.status == 'seckillsg':
            # 抢购中
            self.text_browser_seckill.append(
                '<font color={}>{} - {}</font>'.format(
                    'green', time.strftime('%H:%M:%S'), msg
                )
            )
            self.text_browser_seckill.moveCursor(self.text_browser_seckill.textCursor().End)
            self.label_seckill.setMovie(self.move_seckill)
            self.move_seckill.start()

            self.push_button_reserve.setEnabled(False)
            self.push_button_seckill.setEnabled(False)
            self.push_button_stop.setEnabled(True)

        elif self.status == 'seckillsp':
            # 抢购停止
            self.text_browser_seckill.append(
                '<font color={}>{} - {}</font>'.format(
                    'blue', time.strftime('%H:%M:%S'), '抢购已停止'
                )
            )
            self.text_browser_seckill.moveCursor(self.text_browser_seckill.textCursor().End)
            self.move_seckill.stop()
            self.label_seckill.setPixmap(QtGui.QPixmap(self.configs['seckillsp_image_file']))

            self.push_button_reserve.setEnabled(True)
            self.push_button_seckill.setEnabled(True)
            self.push_button_stop.setEnabled(False)

        elif self.status == 'seckilled':
            # 抢购成功
            self.text_browser_seckill.append(
                '<font color={}>{} - {}</font>'.format(
                    'green', time.strftime('%H:%M:%S'), '抢购成功'
                )
            )
            self.text_browser_seckill.moveCursor(self.text_browser_seckill.textCursor().End)
            self.move_seckill.stop()
            self.label_seckill.setPixmap(QtGui.QPixmap(self.configs['seckillsp_image_file']))

            self.push_button_reserve.setEnabled(True)
            self.push_button_seckill.setEnabled(False)
            self.push_button_stop.setEnabled(False)

            self.dialog_celebrate.setWindowModality(QtCore.Qt.ApplicationModal)
            self.dialog_celebrate.show()
        return

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.signal_close.emit()
        return