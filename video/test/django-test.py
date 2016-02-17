# coding=utf-8
from __future__ import unicode_literals

from AutoSystem.settings import YOUTUBE_DOWNLOAD_DIR
from video.function.file import get_size, clean_media_root


__author__ = 'GoTop'

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoSystem.settings")
django.setup()

# get_video_info(video_id = 'QTCJJiZrNYo')

clean_media_root(max_size=10 * 1024 * 1024, num=1)
