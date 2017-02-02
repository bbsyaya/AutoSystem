# coding=utf-8
from __future__ import unicode_literals, absolute_import

from django.shortcuts import render_to_response

from video.function.youtube_playlist import get_youtube_playlist_video_info, \
    get_youtube_playlist_info

__author__ = 'GoTop'


def get_youtube_playlist_info_view(request, youtube_channel_id,
                                   max_results=50):
    """
    获取youtube channel的playlist信息，并保存
    :param request:
    :param youtube_playlist_id:
    :param max_results:
    :return:
    """
    result = get_youtube_playlist_info(youtube_channel_id, max_results,
                                       request.user)
    if result:
        playlist_list = result
        text = 'YouTube Playlist' + youtube_channel_id + \
               '的信息（包括其playlist的信息）已保存'
    else:
        playlist_list = []
        text = '获取youtube channel的playlist信息失败,原因是无法获取到youtube服务'

    return render_to_response('result.html',
                              {'text': text,
                               'dict_in_list': playlist_list})


def get_youtube_playlist_video_info_view(request, youtube_playlist_id,
                                         max_results=50):
    """
    获取youtube_playlist_id的所有video的信息,并保存
    :param request:
    :param youtube_playlist_id:
    :param max_results:
    :return:
    """
    result = get_youtube_playlist_video_info(youtube_playlist_id, max_results)
    if result:
        video_list = result
        text = 'YouTube Playlist' + youtube_playlist_id + '的视频已保存'
    else:
        video_list = []
        text = '获取youtube视频信息失败'

    return render_to_response('result.html',
                              {'text': text,
                               'dict_in_list': video_list})
