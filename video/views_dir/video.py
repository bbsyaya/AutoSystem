# coding=utf-8
from __future__ import unicode_literals, absolute_import

from django.shortcuts import render_to_response

from video.function.video import download_upload_video
from video.function.youku_playlist import download_playlist_video

__author__ = 'GoTop'


def download_upload_video_view(request, video_id):
    (video_filepath, subtitle_fielpath_list, youku_video_id) = download_upload_video(video_id)

    if video_filepath:
        video_filepath_text = "下载youtube视频成功， 文件地址为: " + video_filepath
    else:
        video_filepath_text = ''

    if subtitle_fielpath_list:
        subtitle_fielpath_text = "下载youtube视频字幕成功， 文件地址为: " + ', '.join(subtitle_fielpath_list)
    else:
        subtitle_fielpath_text = ''
    if youku_video_id:
        youku_video_text = "将视频上传到youku成功， youku_video_id为: " + youku_video_id
    else:
        video_filepath_text = ''

    return render_to_response('result.html',
                              {'text': video_filepath_text + '\n' +
                                       subtitle_fielpath_text + '\n' +
                                       youku_video_text}
                              )

def download_playlist_video_view(request, num):
    """
    下载config model中设置好的youtube playlist中的num个视频，并上传到优酷，设置其playlist
    :param request:
    :param num:
    :return:
    """
    result = download_playlist_video(num, request.user)
    if result:
        return render_to_response('result.html', {'text': '下载并上传指定youtube '
                                                          'playlist的视频成功。',
                                                  'dict_items': result})
    else:
        return render_to_response('result.html', {'text': '未下载并上传指定youtube '
                                                          'playlist的视频，情况1：无需下载'})