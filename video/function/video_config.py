# coding=utf-8
from __future__ import unicode_literals, absolute_import

from video.models import VideoConfig

__author__ = 'GoTop'


def download_video(num):
    config = VideoConfig.objects.filter(is_enable = True)

