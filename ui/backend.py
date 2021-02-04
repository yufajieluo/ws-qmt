#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2021 WShuai, Inc.
# All Rights Reserved.

# @File: backend.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2021/1/21 15:08

import os
import sys
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
import json
import time
import asyncio
import pyppeteer
import multiprocessing
from lxml import etree
from PyQt5 import QtCore

from service.jdSeckill import JdSeckill

class Init(QtCore.QThread):
    signal_cookie = QtCore.pyqtSignal(str)
    signal_eidfp = QtCore.pyqtSignal(str)

    def __init__(self, parent = None, handlers = None):
        super(Init, self).__init__(parent)
        self.handlers = handlers
        return

    def run(self):
        print('--init')
        self.handlers['seckill_handler'].qrlogin.refresh_login_status()
        if self.handlers['seckill_handler'].qrlogin.is_login:
            self.handlers['seckill_handler'].nick_name = self.handlers['seckill_handler'].get_username()
            result = {'ret': True}
        else:
            result = {'ret': False}
        self.signal_cookie.emit(json.dumps(result))

        eid, fp = asyncio.run(self.get_eid_fp())
        print('eid is {}, fp is {}'.format(eid, fp))
        result = {'eid': eid, 'fp': fp}
        self.signal_eidfp.emit(json.dumps(result))
        return

    async def get_eid_fp(self):
        eid = None
        fp = None
        try:
            url = os.path.join(os.getcwd(), self.handlers['seckill_handler'].configs['eidfp_file'])
            if os.path.isfile(url):
                browser = await pyppeteer.launch(
                    {
                        'headless': True,
                        'dumpio': True,
                        'autoClose': True,
                        'handleSIGINT': False,
                        'handleSIGTERM': False,
                        'handleSIGHUP': False
                    }
                )
                page = await browser.newPage()
                await page.goto(url)
                time.sleep(5)
                content = await page.content()
                await page.close()
                await browser.close()

                content_tree = etree.HTML(content)
                eid = content_tree.xpath('//div[@id="eid"]/text()')[0]
                fp = content_tree.xpath('//div[@id="fp"]/text()')[0]
            else:
                self.handlers['seckill_handler'].logger.error('eidfp_file {} is not exist'.format(url))
        except Exception as e:
            self.handlers['seckill_handler'].logger.error('get eid fp Exception: {}'.format(e))
        return eid, fp

class QrCode(QtCore.QThread):
    signal_qrcode = QtCore.pyqtSignal(str)
    signal_login = QtCore.pyqtSignal(str)

    def __init__(self, parent = None, handlers = None):
        super(QrCode, self).__init__(parent)
        self.handlers = handlers
        return

    def run(self):
        qr_code_image = self.handlers['seckill_handler'].get_qr_code()
        self.signal_qrcode.emit(qr_code_image)

        result = self.handlers['seckill_handler'].get_qr_ticket()
        if result['ret']:
            self.handlers['seckill_handler'].save_cookie()
        self.signal_login.emit(json.dumps(result))
        return

class Reserve(QtCore.QThread):
    signal_reserve = QtCore.pyqtSignal(str)

    def __init__(self, parent = None, handlers = None):
        super(Reserve, self).__init__(parent)
        self.article = None
        self.handlers = handlers
        return

    def set_article(self, article):
        self.article = article
        return

    def run(self):
        self.handlers['seckill_handler'].refresh_dynamic_parameters(
            self.article['id'],
            self.article['num'],
            self.article['time']
        )
        result = self.handlers['seckill_handler']._reserve()
        self.signal_reserve.emit(json.dumps(result))
        return

class Seckill(QtCore.QThread):
    signal_sekill = QtCore.pyqtSignal(str)

    def __init__(self, parent = None, handlers = None):
        super(Seckill, self).__init__(parent)
        self.article = None
        self.eid = None
        self.fp = None
        self.handlers = handlers

        self.cpu_core_num = multiprocessing.cpu_count()
        self.pool = None
        return

    def set_article(self, article):
        self.article = article
        return

    def set_eid_fp(self, eid_fp):
        try:
            self.eid = eid_fp['eid']
            self.fp = eid_fp['fp']
        except Exception as e:
            self.handlers['seckill_handler'].logger.error('set eid fp Exception: {}'.format(e))
        return

    def run(self):
        try:
            if self.eid and self.fp:
                self.pool = multiprocessing.Pool(self.cpu_core_num)
                for _ in range(self.cpu_core_num):
                    self.pool.apply_async(
                        process,
                        kwds={
                            'eid': self.eid,
                            'fp': self.fp,
                            'article': self.article,
                            'configs': self.handlers['seckill_handler'].configs
                        },
                        callback=self.result
                    )
                self.pool.close()
                self.pool.join()
                self.stop('timeout')
                #signal = {'msg': 'start'}
                #self.signal_sekill.emit(json.dumps(signal))
            else:
                self.handlers['seckill_handler'].logger.error('self.eid or self.fp is null')
        except Exception as e:
            self.handlers['seckill_handler'].logger.error('startup seckill process Exception: {}'.format(e))

        return

    def result(self, result):
        if result:
            self.stop('success')
        return

    def stop(self, type):
        self.pool.terminate()
        signal = {'type': type}
        self.signal_sekill.emit(json.dumps(signal))
        return

def process(**kwargs):
    jd_seckill = JdSeckill(kwargs['configs'])
    jd_seckill.refresh_dynamic_parameters(
        kwargs['article']['id'],
        kwargs['article']['num'],
        kwargs['article']['time']
    )
    jd_seckill.get_js_parameters(kwargs['eid'], kwargs['fp'])
    jd_seckill._seckill()
    return