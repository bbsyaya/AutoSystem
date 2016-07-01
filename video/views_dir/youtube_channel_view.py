# coding=utf-8
from __future__ import unicode_literals, absolute_import

from django.shortcuts import render_to_response

from video.function.youtube_channel import get_youtube_channel_info

__author__ = 'GoTop'

def get_youtube_channel_info_view(request, channel_id):
    """
    根据channel_id,获取channel的信息，并保存到数据库中
    :param request:
    :param channel:
    :return:
    """
    # todo 未测试
    result = get_youtube_channel_info(channel_id, request.user)
    if result:
        channel_info = result
        text = 'youtube channel ' + channel_id + '的信息已保存'
    else:
        channel_info = []
        text = '获取youtube channel的信息失败'

    return render_to_response('result.html',
                              {'text': text,
                               'dict_in_list': channel_info})
