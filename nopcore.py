#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Module: default
# Author: Docee
# Filename: nopcore.py
# Created on: 2016.1.5

import httplib
import json


class NOPCore(object):
    def __init__(self, base_url):

        self.httpClient = httplib.HTTPConnection(base_url, 80, timeout=30)

    # 向接口请求数据(私有)
    def __requestAPI(self, url):

        # 请求网络数据
        try:
            self.httpClient.request('GET', url)
        except:
            self.httpClient.close()
            raise Exception("网络异常!")

        # 获取返回结果
        response = self.httpClient.getresponse()
        status = response.status

        try:

            if status == 200:

                json_data = json.loads(response.read())

                api_status = json_data['status']

                if api_status != 'success':
                    reason = "NOP服务器异常:", json_data['reason']

                    raise Exception(reason)

                # print jsonData

                return json_data['result']

            else:

                raise Exception("服务器异常!")

        finally:

            if self.httpClient: self.httpClient.close()

    # 获取视频列表
    def requestVideoList(self, category, page=1):

        '''

        获取视频列表

        categroy:视频分类,从0-5
        page:为页码,大于等于1

        '''

        url = "/videolist?category=%s&page=%s" % (category, page)

        # 请求数据
        return self.__requestAPI(url)

    # 获取视频地址
    def requestVideo(self, viewkey):

        """

        获取视频播放地址
        获取到的地址并不是永久的,估计半个小时左右就失效了

        viewkey:视频唯一码,通过视频列表获取

        """

        url = '/viewkey/%s' % viewkey

        # 请求数据
        return self.__requestAPI(url)
