# coding=utf-8
#from __future__ import unicode_literals
import base64
import os
import subprocess

__author__ = 'GoTop'


filename = "E:\media\Video\YouTube\PlayStation_2016_Predictions_-_Kinda_Funny_Gamescast_Ep._51_Pt._3-g8MIFkLq7A8.en.vtt"

filename_basename = os.path.basename(filename)
filename_list = os.path.splitext(filename_basename)

print(filename_basename)
print(filename_list)

