# coding=utf-8
from __future__ import unicode_literals, absolute_import
from django.shortcuts import render_to_response
from video.function.youtube_playlist import get_youtube_playlist_video_info, \
    get_youtube_playlist_info, auto_get_youtube_playlist_video_info
from video.function.youtube_video_info import get_multi_youtube_video_info

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
    result, result_text = get_youtube_playlist_video_info(youtube_playlist_id,
                                                          max_results)
    if result:
        video_list = result
    else:
        video_list = []

    return render_to_response('result.html',
                              {'text': result_text,
                               'dict_in_list': video_list})


def auto_get_youtube_playlist_video_info_view(request):
    """
    在数据库中查找出所有is_download属性设置为true的youtube playlist对象
    下载这些youtube playlist里的视频信息（并获取视频时长等详细信息）并保存到数据库中
    :param request:
    :return:
    """
    #下载playlist的视频信息
    getted_video_list, getted_youtube_playlist_list = auto_get_youtube_playlist_video_info()

    #获取最新下载视频的时长等详细信息
    get_multi_youtube_video_info()
    return render_to_response('result.html',
                              {'text': "成功下载is_download属性设置为true的youtube "
                                       "playlist里的视频信息并保存到数据库中",
                               'list': getted_youtube_playlist_list
                               })
