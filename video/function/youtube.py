# coding=utf-8
from __future__ import unicode_literals

__author__ = 'GoTop'

import youtube_upload, pafy

def get_youtube_video_id(url):

    myvid = pafy.new("http://www.youtube.com/watch?v=dQw4w9WgXc")