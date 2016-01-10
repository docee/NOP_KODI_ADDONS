#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Module: default
# Author: Docee
# Filename: nop.py
# Created on: 2016.1.5

import sys
from nopcore import NOPCore
import xbmcplugin
import xbmcgui
import xbmc
from urlparse import parse_qsl

_url = sys.argv[0]
_handle = int(sys.argv[1])

CATEGORYS = ["最近得分","收藏最多","最近加精","本月最热","上月最热"]

# 初始化NOP服务器地址
core = NOPCore("nop.skyworth.wang")


# 列出视频类别
def list_category(categorys):

    lists = []

    for i in range(0,len(categorys)):

        list_item = xbmcgui.ListItem(label=categorys[i])

        url = '{0}?action=list&category={1}&page=1'.format(_url,i)

        lists.append((url,list_item,True))

    xbmcplugin.addDirectoryItems(_handle, lists, len(lists))
    # xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

# 列出视频列表
def list_category_videos(categoryIndex,page):

    try:
        result = core.requestVideoList(categoryIndex,page)

        videos = result['videos']

        lists = []

        for i in range(0,len(videos)):
            title = videos[i]['title']

            duration_strings = videos[i]['duration'].split(':')

            duration = int(duration_strings[0]) * 60 + int(duration_strings[1])

            list_item = xbmcgui.ListItem(label=title,thumbnailImage=videos[i]['screenshot'][0])
            list_item.setInfo('video',{'title':title,'duration':duration})
            list_item.setProperty('IsPlayable','true')

            url = '{0}?action=viewkey&viewkey={1}'.format(_url,videos[i]['viewkey'])

            lists.append((url,list_item,False))

        xbmcplugin.addDirectoryItems(_handle, lists, len(lists))
        # xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(_handle)

    except:

        #TODO 获取视频失败异常处理(暂时不处理)
        pass


# 获取视频地址并播放
def get_video(viewkey):

    try:
        result = core.requestVideo(viewkey)

        url = result['url']

        play_item = xbmcgui.ListItem(path=url)

        xbmcplugin.setResolvedUrl(_handle,True,listitem=play_item)
        # xbmc.Player.play(item=play_item)


    except:
        #TODO 播放视频失败异常处理(暂时不处理)
        pass


# 路由
def router(paramstring):

    # 解析QueryString
    params = dict(parse_qsl(paramstring))

    if params:

        # 获取视频列表
        if params['action'] == 'list':
            category = int(params['category'])
            page = int(params['page'])

            list_category_videos(category,page)

        # 获取视频播放地址
        elif params['action'] == 'viewkey':
            viewkey = params['viewkey']
            get_video(viewkey)

    else:
        # 获取视频分类
        list_category(CATEGORYS)

# 程序主入口
if __name__ == '__main__':
    router(sys.argv[2][1:])