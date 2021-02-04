#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2021 WShuai, Inc.
# All Rights Reserved.

# @File: spiderSession.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2021/1/21 10:09

import os
import pickle
import requests

class SpiderSession(object):
    """
    Session相关操作
    """
    def __init__(self, default_user_agent = None, cookie_path = None):
        self.cookies_dir_path = cookie_path
        self.user_agent = default_user_agent
        self.headers = {
            "User-Agent": default_user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;"
                      "q=0.9,image/webp,image/apng,*/*;"
                      "q=0.8,application/signed-exchange;"
                      "v=b3",
            "Connection": "keep-alive"
        }
        self.session = requests.session()
        self.session.headers = self.headers
        return

    def get_headers(self):
        return self.headers

    def get_user_agent(self):
        return self.user_agent

    def get_session(self):
        """
        获取当前Session
        :return:
        """
        return self.session

    def load_cookies_from_local(self):
        """
        从本地加载Cookie
        :return:
        """
        cookies_file = None
        result = False
        if os.path.exists(self.cookies_dir_path):
            for name in os.listdir(self.cookies_dir_path):
                if name.endswith(".cookies"):
                    cookies_file = os.path.join(self.cookies_dir_path, name)
                    break
            if cookies_file:
                with open(cookies_file, 'rb') as f:
                    local_cookies = pickle.load(f)
                self.session.cookies.update(local_cookies)
                result = True
        return result

    def save_cookies_to_local(self, cookie_file_name):
        """
        保存Cookie到本地
        :param cookie_file_name: 存放Cookie的文件名称
        :return:
        """
        cookies_file = os.path.join(self.cookies_dir_path, '{}.cookies'.format(cookie_file_name))
        directory = os.path.dirname(cookies_file)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(cookies_file, 'wb') as f:
            pickle.dump(self.session.cookies, f)
