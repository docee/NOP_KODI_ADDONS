#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Module: default
# Author: Docee
# Filename: nop.py
# Created on: 2016.1.5

import sys
from nopcore import  NOP_Core
import xbmcplugin
import xbmcgui
from urlparse import parse_qsl

_url = sys.argv[0]
_handle = int(sys.argv[1])

CATEGORYS = ["最近得分","收藏最多","最近加精","本月最热","上月最热"]

# 初始化NOP服务器地址
core = NOP_Core("nop.skyworth.wang")


# 列出视频类别
def list_category(categorys):

    lists = []

    for i in range(0,len(categorys)):

        list_item = xbmcgui.ListItem(label=categorys[i])

        url = '{0}?action=list&category={1}'.format(_url,i)

        lists.append((url,list_item,True))

    xbmcplugin.addDirectoryItem(_handle, lists, len(lists))
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

# 列出视频列表
def list_category_videos(categoryIndex,page):

    try:
        result = core.requestVideoList(categoryIndex,page)
    except:

        #TODO
        pass



# 路由
def router(paramstring):

    # 解析QueryString
    params = dict(parse_qsl(paramstring))

    if params:

        if params['action'] == 'list':
            #TODO
            pass
        elif params['action'] == 'viewkey':
            #TODO
            pass
        elif params['action'] == 'play':
            #TODO
            pass
        else:
            list_category(CATEGORYS)

# 程序主入口
if __name__ == '__main__':
    router(sys.argv[2][1:])