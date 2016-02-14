# coding=utf-8
from __future__ import unicode_literals

from video.function.youtube import get_video_info

__author__ = 'GoTop'

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoSystem.settings")
django.setup()


get_video_info(video_id = 'QTCJJiZrNYo')


