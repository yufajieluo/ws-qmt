#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2021 WShuai, Inc.
# All Rights Reserved.

# @File: qrlogin.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2021/1/21 10:07

import os
import time
import json
import random
import requests

class QrLogin(object):
    """
    扫码登录
    """
    def __init__(self, session, headers, user_agent, qrcode_img_file, logger, util):
        """
        初始化扫码登录
        大致流程：
            1、访问登录二维码页面，获取Token
            2、使用Token获取票据
            3、校验票据
        """
        self.logger = logger
        self.util = util
        self.qrcode_img_file = qrcode_img_file

        self.session = session
        self.headers = headers
        self.user_agent = user_agent

        self.is_login = False
        self.refresh_login_status()

    def refresh_login_status(self):
        """
        刷新是否登录状态
        :return:
        """
        self.is_login = self._validate_cookies()

    def _validate_cookies(self):
        """
        验证cookies是否有效（是否登陆）
        通过访问用户订单列表页进行判断：若未登录，将会重定向到登陆页面。
        :return: cookies是否有效 True/False
        """
        url = 'https://order.jd.com/center/list.action'
        payload = {
            'rid': str(int(time.time() * 1000)),
        }
        try:
            resp = self.session.get(url=url, params=payload, allow_redirects=False)
            #print('resp is {}'.format(resp.text))
            if resp.status_code == requests.codes.OK:
                return True
        except Exception as e:
            self.logger.error("验证cookies是否有效发生异常", e)
        return False

    def _get_login_page(self):
        """
        获取PC端登录页面
        :return:
        """
        url = "https://passport.jd.com/new/login.aspx"
        page = self.session.get(url, headers=self.headers)
        return page

    def _get_qrcode(self):
        """
        缓存并展示登录二维码
        :return:
        """
        url = 'https://qr.m.jd.com/show'
        payload = {
            'appid': 133,
            'size': 300,
            't': str(int(time.time() * 1000)),
        }
        headers = {
            'User-Agent': self.user_agent,
            'Referer': 'https://passport.jd.com/new/login.aspx',
        }
        resp = self.session.get(url=url, headers=headers, params=payload)

        if not self.util.response_status(resp):
            self.logger.info('获取二维码失败')
            return False

        self.util.save_image(resp, self.qrcode_img_file)
        self.logger.info('二维码获取成功，请打开京东APP扫描')

        #self.util.open_image(self.util.add_bg_for_qr(self.qrcode_img_file))
        #if global_config.getRaw('messenger', 'email_enable') == 'true':
        #    email.send('二维码获取成功，请打开京东APP扫描', "<img src='cid:qr_code.png'>", [email.mail_user], 'qr_code.png')
        return self.qrcode_img_file

    def _get_qrcode_ticket(self):
        """
        通过 token 获取票据
        :return:
        """
        url = 'https://qr.m.jd.com/check'
        payload = {
            'appid': '133',
            'callback': 'jQuery{}'.format(random.randint(1000000, 9999999)),
            'token': self.session.cookies.get('wlfstk_smdl'),
            '_': str(int(time.time() * 1000)),
        }
        headers = {
            'User-Agent': self.user_agent,
            'Referer': 'https://passport.jd.com/new/login.aspx',
        }
        resp = self.session.get(url=url, headers=headers, params=payload)

        if not self.util.response_status(resp):
            self.logger.error('获取二维码扫描结果异常')
            return False

        resp_json = self.util.parse_json(resp.text)
        if resp_json['code'] != 200:
            self.logger.info('Code: %s, Message: %s', resp_json['code'], resp_json['msg'])
            return None
        else:
            self.logger.info('已完成手机客户端确认')
            return resp_json['ticket']

    def _validate_qrcode_ticket(self, ticket):
        """
        通过已获取的票据进行校验
        :param ticket: 已获取的票据
        :return:
        """
        url = 'https://passport.jd.com/uc/qrCodeTicketValidation'
        headers = {
            'User-Agent': self.user_agent,
            'Referer': 'https://passport.jd.com/uc/login?ltype=logout',
        }

        resp = self.session.get(url=url, headers=headers, params={'t': ticket})
        if not self.util.response_status(resp):
            return False

        resp_json = json.loads(resp.text)
        if resp_json['returnCode'] == 0:
            return True
        else:
            self.logger.info(resp_json)
            return False

    def login_by_qrcode(self):
        """
        二维码登陆
        :return:
        """
        self.get_qrcode()
        self.get_qrticket()
        return

    def get_qrcode(self):
        self._get_login_page()
        qr_code_image = self._get_qrcode()
        return qr_code_image

    def get_qrticket(self):
        # get QR code ticket
        result = {'ret': None, 'msg': None}
        ticket = None
        retry_times = 85
        #retry_times = 5
        for _ in range(retry_times):
            ticket = self._get_qrcode_ticket()
            if ticket:
                # validate QR code ticket
                if not self._validate_qrcode_ticket(ticket):
                    # raise Exception('二维码信息校验失败')
                    result = {'ret': False, 'msg': '二维码校验失败'}
                else:
                    self.refresh_login_status()
                    self.logger.info('二维码登录成功')
                    result = {'ret': True, 'msg': '二维码登录成功'}
                break
            else:
                time.sleep(2)
        else:
            #raise Exception('二维码过期，请重新获取扫描')
            result = {'ret': False, 'msg': '二维码过期'}
        os.remove(self.qrcode_img_file)
        return result