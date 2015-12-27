# coding=utf-8
from __future__ import unicode_literals

__author__ = 'GoTop'

import pysrt

"""
合并两种不同言语的字幕
参考 https://github.com/byroot/pysrt/issues/15
https://github.com/byroot/pysrt/issues/17

展示没心情弄，有空再说
2015-12-27
"""

sub_en = "E:\Fallout 4 Mods - Santa Claus Power Armor-z0zvQfLOcLM.en.srt"
sub_cn = "E:\Fallout 4 Mods - Santa Claus Power Armor-z0zvQfLOcLM.zh-Hans.srt"


subs = pysrt.open(sub_en)

