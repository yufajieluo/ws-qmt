#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2021 WShuai, Inc.
# All Rights Reserved.

# @File: jdSeckill.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2021/1/21 10:29

import os
import sys
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
import time
import random
import functools
from lxml import html
from datetime import datetime, timedelta
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, wait

from .util import Util
from .timer import Timer
from .qrlogin import QrLogin
from .spiderSession import SpiderSession
from common import commLog

class JdSeckill(object):
    def __init__(self, configs, logger = None):
        self.configs = configs
        if not logger:
            log_handler = commLog.LogHandler(configs['logging'])
            log_path = os.path.dirname(configs['logging']['handlers']['default']['filename'])
            if not os.path.isdir(log_path):
                os.makedirs(log_path)
            #self.logger = log_handler.register_rotate('{}-{}'.format(self.__class__.__name__.lower(), os.getpid()))
            self.logger = log_handler.register_rotate('{}-{}'.format(self.__class__.__name__.lower(), 'real'))
            self.logger.info('service config is {}'.format(configs))
        else:
            self.logger = logger

        if not os.path.isdir(self.configs['cookie_path']):
            os.makedirs(self.configs['cookie_path'])

        self.spider_session = SpiderSession(
            default_user_agent = self.configs['default_user_agent'],
            cookie_path = self.configs['cookie_path']
        )
        self.spider_session.load_cookies_from_local()

        self.util = Util()
        self.qrlogin = QrLogin(
            self.spider_session.get_session(),
            self.spider_session.get_headers(),
            self.spider_session.get_user_agent(),
            os.path.join(self.configs['cookie_path'], self.configs['qr_code_file']),
            logger,
            self.util
        )

        print('classs JdSeckill self.qrlogin.is_login is {}'.format(self.qrlogin.is_login))

        # 初始化信息
        self.sku_id = None
        self.seckill_num = None
        self.buy_time = None
        self.eid = None
        self.fp = None

        self.seckill_init_info = dict()
        self.seckill_url = dict()
        self.seckill_order_data = dict()
        self.timers = None

        self.session = self.spider_session.get_session()
        self.user_agent = self.spider_session.user_agent
        self.nick_name = None

        self.running_flag = True

    def refresh_dynamic_parameters(self, sku_id, seckill_num, buy_time):
        self.sku_id = sku_id
        self.seckill_num = seckill_num
        self.buy_time = buy_time
        self.timers = Timer(self.buy_time, self.logger)
        return

    def get_js_parameters(self, eid, fp):
        self.eid = eid
        self.fp = fp
        return

    def login_by_qrcode(self):
        """
        二维码登陆
        :return:
        """
        if self.qrlogin.is_login:
            self.logger.info('登录成功')
            return

        self.qrlogin.login_by_qrcode()

        if self.qrlogin.is_login:
            self.nick_name = self.get_username()
            self.spider_session.save_cookies_to_local(self.nick_name)
        else:
            raise Exception("二维码登录失败！")


    def check_login_and_jdtdufp(func):
        """
        用户登陆态校验装饰器。若用户未登陆，则调用扫码登陆
        """

        @functools.wraps(func)
        def new_func(self, *args, **kwargs):
            print('login is {}'.format(self.qrlogin.is_login))
            if not self.qrlogin.is_login:
                self.logger.info("{0} 需登陆后调用，开始扫码登陆".format(func.__name__))
                self.login_by_qrcode()
            return func(self, *args, **kwargs)

        return new_func

    @check_login_and_jdtdufp
    def reserve(self):
        """
        预约
        """
        self._reserve()

    #@check_login_and_jdtdufp
    def seckill_by_proc_pool(self, work_count=1):
        """
        多进程进行抢购
        work_count：进程数量
        """
        with ProcessPoolExecutor(work_count) as pool:
            for i in range(work_count):
                pool.submit(self._seckill)
        return

    def _reserve(self):
        """
        预约
        """
        return self.make_reserve()

    def seckill(self, work_count = 3):
        tasks = []
        with ThreadPoolExecutor(work_count) as pool:
            for _ in range(work_count):
                task = pool.submit(self._seckill)
                tasks.append(task)
        wait(tasks)
        return

    def _seckill(self):
        """
        抢购
        """

        result = False
        while self.running_flag:
            self.seckill_canstill_running()
            try:
                self.request_seckill_url()
                while self.running_flag:
                    self.request_seckill_checkout_page()
                    if self.submit_seckill_order():
                        result = True
                        break
                    else:
                        self.seckill_canstill_running()
                        continue
            except Exception as e:
                self.logger.info('抢购发生异常，稍后继续执行！', e)
            self.util.wait_some_time()
        '''
        while True:
            try:
                init = self._get_seckill_init_info()
                print('init info is {}'.format(init))
            except Exception as e:
                print('init Exception is {}'.format(e))
            time.sleep(30)
        '''
        return result

    def seckill_canstill_running(self):
        """用config.ini文件中的continue_time加上函数buytime_get()获取到的buy_time，
            来判断抢购的任务是否可以继续运行
        """
        buy_time = self.timers.buytime_get()
        continue_time = self.configs['continue_time']
        stop_time = datetime.strptime(
            (buy_time + timedelta(minutes=continue_time)).strftime("%Y-%m-%d %H:%M:%S.%f"),
            "%Y-%m-%d %H:%M:%S.%f"
        )
        current_time = datetime.now()
        self.logger.info('current_time is {}, stop_time is {}'.format(current_time, stop_time))
        if current_time > stop_time:
            self.running_flag = False
            self.logger.info('超过允许的运行时间，任务结束。')

    def make_reserve(self):
        """商品预约"""
        self.logger.info('商品名称:{}'.format(self.get_sku_title()))
        url = 'https://yushou.jd.com/youshouinfo.action?'
        payload = {
            'callback': 'fetchJSON',
            'sku': self.sku_id,
            '_': str(int(time.time() * 1000)),
        }
        headers = {
            'User-Agent': self.user_agent,
            'Referer': 'https://item.jd.com/{}.html'.format(self.sku_id),
        }
        resp = self.session.get(url=url, params=payload, headers=headers)
        resp_json = self.util.parse_json(resp.text)
        reserve_url = resp_json.get('url')

        result = None
        for _ in range(10):
            try:
                self.session.get(url='https:' + reserve_url)
                self.logger.info('预约成功，已获得抢购资格 / 您已成功预约过了，无需重复预约')
                #if global_config.getRaw('messenger', 'server_chan_enable') == 'true':
                #    success_message = "预约成功，已获得抢购资格 / 您已成功预约过了，无需重复预约"
                #    send_wechat(success_message)
                result = {'ret': True, 'msg': '预约成功'}
                break
            except Exception as e:
                self.logger.error('预约失败正在重试...')
                time.sleep(2)
        else:
            result = {'ret': False, 'msg': '预约失败，请确认预约信息'}
            self.logger.error('超过最大重试次数，预约失败')
        return result

    def get_username(self):
        """获取用户信息"""
        url = 'https://passport.jd.com/user/petName/getUserInfoForMiniJd.action'
        payload = {
            'callback': 'jQuery{}'.format(random.randint(1000000, 9999999)),
            '_': str(int(time.time() * 1000)),
        }
        headers = {
            'User-Agent': self.user_agent,
            'Referer': 'https://order.jd.com/center/list.action',
        }

        resp = self.session.get(url=url, params=payload, headers=headers)

        try_count = 5
        while not resp.text.startswith("jQuery"):
            try_count = try_count - 1
            if try_count > 0:
                resp = self.session.get(url=url, params=payload, headers=headers)
            else:
                break
            self.util.wait_some_time()
        # 响应中包含了许多用户信息，现在在其中返回昵称
        # jQuery2381773({"imgUrl":"//storage.360buyimg.com/i.imageUpload/xxx.jpg","lastLoginTime":"","nickName":"xxx","plusStatus":"0","realName":"xxx","userLevel":x,"userScoreVO":{"accountScore":xx,"activityScore":xx,"consumptionScore":xxxxx,"default":false,"financeScore":xxx,"pin":"xxx","riskScore":x,"totalScore":xxxxx}})
        return self.util.parse_json(resp.text).get('nickName')

    def get_sku_title(self):
        """获取商品名称"""
        url = 'https://item.jd.com/{}.html'.format(self.sku_id)
        resp = self.session.get(url).content
        etree = html.etree
        x_data = etree.HTML(resp)
        sku_title = x_data.xpath('/html/head/title/text()')
        return sku_title[0]

    def get_seckill_url(self):
        """获取商品的抢购链接
        点击"抢购"按钮后，会有两次302跳转，最后到达订单结算页面
        这里返回第一次跳转后的页面url，作为商品的抢购链接
        :return: 商品的抢购链接
        """
        url = 'https://itemko.jd.com/itemShowBtn'
        payload = {
            'callback': 'jQuery{}'.format(random.randint(1000000, 9999999)),
            'skuId': self.sku_id,
            'from': 'pc',
            '_': str(int(time.time() * 1000)),
        }
        headers = {
            'User-Agent': self.user_agent,
            'Host': 'itemko.jd.com',
            'Referer': 'https://item.jd.com/{}.html'.format(self.sku_id),
        }
        index = 0
        while True:
            if index >= 100:
                self.logger.info('100')
                self.seckill_canstill_running()
                if not self.running_flag:
                    self.logger.error('时间到')
                    return None
                else:
                    self.logger.error('时间未到')
                    index = 0

            resp = self.session.get(url=url, headers=headers, params=payload)
            resp_json = self.util.parse_json(resp.text)
            if resp_json.get('url'):
                # https://divide.jd.com/user_routing?skuId=8654289&sn=c3f4ececd8461f0e4d7267e96a91e0e0&from=pc
                router_url = 'https:' + resp_json.get('url')
                # https://marathon.jd.com/captcha.html?skuId=8654289&sn=c3f4ececd8461f0e4d7267e96a91e0e0&from=pc
                seckill_url = router_url.replace(
                    'divide', 'marathon').replace(
                    'user_routing', 'captcha.html')
                self.logger.info("抢购链接获取成功: %s", seckill_url)
                return seckill_url
            else:
                index += 1
                self.logger.info("抢购链接获取失败，稍后自动重试")
                self.util.wait_some_time()


    def request_seckill_url(self):
        """访问商品的抢购链接（用于设置cookie等"""
        self.logger.info('用户:{}'.format(self.get_username()))
        self.logger.info('商品名称:{}'.format(self.get_sku_title()))
        self.timers.start()
        url = self.get_seckill_url()
        if url:
            self.seckill_url[self.sku_id] = url
            self.logger.info('访问商品的抢购连接...')
            headers = {
                'User-Agent': self.user_agent,
                'Host': 'marathon.jd.com',
                'Referer': 'https://item.jd.com/{}.html'.format(self.sku_id),
            }
            self.session.get(
                url=self.seckill_url.get(
                    self.sku_id),
                headers=headers,
                allow_redirects=False)
        return

    def request_seckill_checkout_page(self):
        """访问抢购订单结算页面"""
        self.logger.info('访问抢购订单结算页面...')
        url = 'https://marathon.jd.com/seckill/seckill.action'
        payload = {
            'skuId': self.sku_id,
            'num': self.seckill_num,
            'rid': int(time.time())
        }
        headers = {
            'User-Agent': self.user_agent,
            'Host': 'marathon.jd.com',
            'Referer': 'https://item.jd.com/{}.html'.format(self.sku_id),
        }
        self.session.get(url=url, params=payload, headers=headers, allow_redirects=False)

    def _get_seckill_init_info(self):
        """获取秒杀初始化信息（包括：地址，发票，token）
        :return: 初始化信息组成的dict
        """
        self.logger.info('获取秒杀初始化信息...')
        url = 'https://marathon.jd.com/seckillnew/orderService/pc/init.action'
        data = {
            'sku': self.sku_id,
            'num': self.seckill_num,
            'isModifyAddress': 'false',
        }
        headers = {
            'User-Agent': self.user_agent,
            'Host': 'marathon.jd.com',
        }
        resp = self.session.post(url=url, data=data, headers=headers)

        resp_json = None
        try:
            resp_json = self.util.parse_json(resp.text)
        except Exception as e:
            self.logger.error('获取秒杀初始化信息失败，返回信息:{}'.format(e))

        return resp_json

    def _get_seckill_order_data(self):
        """生成提交抢购订单所需的请求体参数
        :return: 请求体参数组成的dict
        """
        self.logger.info('生成提交抢购订单所需参数...')
        # 获取用户秒杀初始化信息
        #self.seckill_init_info[self.sku_id] = self._get_seckill_init_info()
        #init_info = self.seckill_init_info.get(self.sku_id)
        init_info = self._get_seckill_init_info()
        if init_info:
            # logger.info('init_info is {}'.format(init_info))
            default_address = init_info['addressList'][0]  # 默认地址dict
            invoice_info = init_info.get('invoiceInfo', {})  # 默认发票信息dict, 有可能不返回
            token = init_info['token']
            data = {
                'skuId': self.sku_id,
                'num': self.seckill_num,
                'addressId': default_address['id'],
                'yuShou': 'true',
                'isModifyAddress': 'false',
                'name': default_address['name'],
                'provinceId': default_address['provinceId'],
                'cityId': default_address['cityId'],
                'countyId': default_address['countyId'],
                'townId': default_address['townId'],
                'addressDetail': default_address['addressDetail'],
                'mobile': default_address['mobile'],
                'mobileKey': default_address['mobileKey'],
                'email': default_address.get('email', ''),
                'postCode': '',
                'invoiceTitle': invoice_info.get('invoiceTitle', -1),
                'invoiceCompanyName': '',
                'invoiceContent': invoice_info.get('invoiceContentType', 1),
                'invoiceTaxpayerNO': '',
                'invoiceEmail': '',
                'invoicePhone': invoice_info.get('invoicePhone', ''),
                'invoicePhoneKey': invoice_info.get('invoicePhoneKey', ''),
                'invoice': 'true' if invoice_info else 'false',
                'password': '',
                'codTimeType': 3,
                'paymentType': 4,
                'areaCode': '',
                'overseas': 0,
                'phone': '',
                'eid': self.eid,
                'fp': self.fp,
                'token': token,
                'pru': ''
            }
        else:
            data = None
        # logger.info("order_date：%s", data)
        return data

    def submit_seckill_order(self):
        """提交抢购（秒杀）订单
        :return: 抢购结果 True/False
        """
        url = 'https://marathon.jd.com/seckillnew/orderService/pc/submitOrder.action'
        payload = {
            'skuId': self.sku_id,
        }

        order_info = self._get_seckill_order_data()
        if not order_info:
            self.logger.error('获取订单信息失败')
            return False

        #try:
        #    self.seckill_order_data[self.sku_id] = self._get_seckill_order_data()
        #except Exception as e:
        #    self.logger.info('抢购失败，无法获取生成订单的基本信息，接口返回:【{}】'.format(str(e)))
        #    return False

        self.logger.info('提交抢购订单...')
        headers = {
            'User-Agent': self.user_agent,
            'Host': 'marathon.jd.com',
            'Referer': 'https://marathon.jd.com/seckill/seckill.action?skuId={0}&num={1}&rid={2}'.format(
                self.sku_id, self.seckill_num, int(time.time())),
        }
        resp = self.session.post(
            url=url,
            params=payload,
            data=self.seckill_order_data.get(
                self.sku_id),
            headers=headers)
        resp_json = None
        try:
            resp_json = self.util.parse_json(resp.text)
        except Exception as e:
            self.logger.info('抢购失败，返回信息:{}'.format(resp.text[0: 128]))
            return False
        # 返回信息
        # 抢购失败：
        # {'errorMessage': '很遗憾没有抢到，再接再厉哦。', 'orderId': 0, 'resultCode': 60074, 'skuId': 0, 'success': False}
        # {'errorMessage': '抱歉，您提交过快，请稍后再提交订单！', 'orderId': 0, 'resultCode': 60017, 'skuId': 0, 'success': False}
        # {'errorMessage': '系统正在开小差，请重试~~', 'orderId': 0, 'resultCode': 90013, 'skuId': 0, 'success': False}
        # 抢购成功：
        # {"appUrl":"xxxxx","orderId":820227xxxxx,"pcUrl":"xxxxx","resultCode":0,"skuId":0,"success":true,"totalMoney":"xxxxx"}
        if resp_json.get('success'):
            order_id = resp_json.get('orderId')
            total_money = resp_json.get('totalMoney')
            pay_url = 'https:' + resp_json.get('pcUrl')
            self.logger.info('抢购成功，订单号:{}, 总价:{}, 电脑端付款链接:{}'.format(order_id, total_money, pay_url))
            #if global_config.getRaw('messenger', 'server_chan_enable') == 'true':
            #    success_message = "抢购成功，订单号:{}, 总价:{}, 电脑端付款链接:{}".format(order_id, total_money, pay_url)
            #    send_wechat(success_message)
            #    self.running_flag = False
            return True
        else:
            self.logger.info('抢购失败，返回信息:{}'.format(resp_json))
            #if global_config.getRaw('messenger', 'server_chan_enable') == 'true':
            #    error_message = '抢购失败，返回信息:{}'.format(resp_json)
            #    send_wechat(error_message)
            return False

    def get_qr_code(self):
        return self.qrlogin.get_qrcode()

    def get_qr_ticket(self):
        return self.qrlogin.get_qrticket()

    def save_cookie(self):
        if self.qrlogin.is_login:
            self.nick_name = self.get_username()
            self.spider_session.save_cookies_to_local(self.get_username())
        return