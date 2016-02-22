# coding=utf-8
from __future__ import unicode_literals, absolute_import

import os

from django.shortcuts import render_to_response

from AutoSystem import settings
from video.function.subtitle import merge_subtitle, \
    add_subtitle_to_video_process, merge_video_subtitle, \
    merge_sub_edit_style
from video.models import Video

__author__ = 'GoTop'

import pysrt
from pysrt import SubRipFile, SubRipItem, SubRipTime


def merge_subtitle_view(request, video_id):
    """
    合并video_id视频的中英字幕

    :param request:
    :param video_id:
    :return:
    """
    merge_subs_dir = merge_video_subtitle(video_id)

    return render_to_response('result.html',
                              {'text': '合并的字幕文件地址为 ' + merge_subs_dir})


def merge_sub_edit_style_view(request, video_id):
    merge_sub_file = merge_sub_edit_style(video_id)

    return render_to_response('result.html',
                              {'text': '合并的字幕文件地址' + merge_sub_file})


def merge_subtitle_to_video_view(request, video_id, sub_lang_type):
    """
    将指定语言类型的字幕合并到video_id的视频中
    :param request:
    :param video_id:
    :param sub_lang_type:
    :return:
    """
    add_subtitle_to_video_process(video_id, sub_lang_type)

    return render_to_response('result.html', {'text': '合并的字幕到视频完成!'})
