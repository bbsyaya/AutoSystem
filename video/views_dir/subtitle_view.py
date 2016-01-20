# coding=utf-8
from __future__ import unicode_literals

import os

from django.shortcuts import render_to_response

from AutoSystem import settings
from video.function.subtile import merge_subtitle
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
    video = Video.objects.get(pk=video_id)

    # Settings default values
    delta = SubRipTime(milliseconds=500)
    encoding = "utf_8"

    subs_cn = SubRipFile.open(video.subtitle_cn, encoding=encoding)
    subs_en = SubRipFile.open(video.subtitle_en, encoding=encoding)
    merge_subs = merge_subtitle(subs_cn, subs_en, delta)

    merge_subs_filename = '%s-%s.zh-Hans.en.srt' % (video.title, video.video_id)

    merge_subs_dir = os.path.join(settings.YOUTUBE_DOWNLOAD_DIR, merge_subs_filename)

    merge_subs.save(merge_subs_dir, encoding=encoding)

    return render_to_response('result.html', {'text': '合并的字幕文件地址为 ' + merge_subs_dir})

