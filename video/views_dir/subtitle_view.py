# coding=utf-8
from __future__ import unicode_literals, absolute_import

import os

from django.shortcuts import render_to_response

from AutoSystem import settings
from video.function.subtitle import merge_subtitle, \
    add_subtitle_to_video_process, merge_video_subtitle, \
    merge_sub_edit_style, change_vtt_to_ass_and_edit_style
from video.models import Video

__author__ = 'GoTop'

import pysrt
from pysrt import SubRipFile, SubRipItem, SubRipTime


def merge_subtitle_view(request, video_id):
    """
    将video_id的中英vtt字幕转换为srt字幕，然后合并为srt格式的字幕

    :param request:
    :param video_id:
    :return:
    """
    merge_subs_dir = merge_video_subtitle(video_id)

    return render_to_response('result.html',
                              {'text': '合并的字幕文件地址为 ' + merge_subs_dir})


def merge_sub_edit_style_view(request, video_id):
    """
    合并中、英字幕（VTT格式）为一个SRT格式字幕文件
    然后转化为ASS格式字幕，并添加字体式样
    :param request:
    :param video_id:
    :return:
    """
    merge_sub_file = merge_sub_edit_style(video_id)

    return render_to_response('result.html',
                              {'text': '合并的字幕文件地址' + merge_sub_file})


def change_vtt_to_ass_and_edit_style_view(request, video_id):
    """
    将video_id对应的Video对象的subtitle_cn指向的中文vtt格式字幕，
    转化为ass格式，保存到subtitle_merge字段
    然后修改ass字幕的文字式样
    :param request:
    :param video_id:
    :return:
    """
    ass_path = change_vtt_to_ass_and_edit_style(video_id)

    return render_to_response('result.html',
                              {'text': 'vtt字幕转化为ass字幕，并添加式样的文件的地址' + ass_path})


def merge_subtitle_to_video_view(request, video_id, mode, sub_lang_type):
    """
    将指定语言类型的字幕合并到video_id的视频中
    :param request:
    :param video_id:
    :param sub_lang_type:
    :return:
    """
    add_subtitle_to_video_process(video_id, mode, sub_lang_type)

    return render_to_response('result.html', {'text': '合并的字幕到视频完成!'})
