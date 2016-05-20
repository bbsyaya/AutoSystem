# coding=utf-8
from __future__ import unicode_literals, absolute_import
import base64
import os
import platform
import re
import subprocess

import math

from AutoSystem.settings import YOUTUBE_DOWNLOAD_DIR
from video.libs.convert_subtitles import convert_file

__author__ = 'GoTop'

# filename = "E:\media\Video\YouTube\PlayStation_2016_Predictions_
# -_Kinda_Funny_Gamescast_Ep._51_Pt._3-g8MIFkLq7A8.en.vtt"
#
# filename_basename = os.path.basename(filename)
# filename_list = os.path.splitext(filename_basename)
#
# print(filename_basename)
# print(filename_list)


# name = 'E:\\media\\Video\\YouTube\\LG K10 and K7 hands-on-_9coAtC2PZI.mkv'
# #name = 'E:\\media\\Video\\YouTube\\out.mkv'
# os.remove(name)

# print platform.system()
#
# import pysubs2
#
# pysubs2.load()

# list2 = [1, 2, 3, 4, 5, 6, 7 ]
# num = 3
# print(list2[:num])

# file = 'E:\\media\\Video\\YouTube\\EVIL_KITTY_CAT_Minecraft_Animation
# -Qnvb_6CG8zM.zh-Hans_en.mkv'
# print(os.path.getsize(file))


# input = 'input.vtt'
# output = 'ouput.srt'
# convert_file(input, output)

# tags = ["Amazon", "new", "march", "shows", "movies", "tv", "Streaming"]
# print(len(tags))

# import json
# tags_list = ''
# print(json.dumps(tags_list))

tag = "tech under $100, $50, $25, $500"
tag = re.sub(ur"[^\u4e00-\u9fa5a-zA-Z0-9]", "", tag)
print tag
