#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2021 WShuai, Inc.
# All Rights Reserved.

# @File: tdudfp.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2021/1/21 10:32

import asyncio

class JdTdudfp:
    def __init__(self, sp):
        self.cookies = sp.get_cookies()
        self.user_agent = sp.get_user_agent()

        self.is_init = False
        self.jd_tdudfp = None

    def init_jd_tdudfp(self):
        self.is_init = True

        loop = asyncio.get_event_loop()
        get_future = asyncio.ensure_future(self._get())
        loop.run_until_complete(get_future)
        self.jd_tdudfp = get_future.result()

    def get(self, key):
        return self.jd_tdudfp.get(key) if self.jd_tdudfp else None

    async def _get(self):
        jd_tdudfp = None
        return jd_tdudfp