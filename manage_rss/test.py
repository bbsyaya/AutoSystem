# coding=utf-8
from __future__ import unicode_literals
from AutoSystem import settings

__author__ = 'GoTop'

#########################################
import pafy

url = "https://www.youtube.com/watch?v=bMt47wvK6u0"

video = pafy.new(url)

print(video.title)


plurl = "https://www.youtube.com/playlist?list=PLNWIWf8IRkr9k-2nkMxb08Q2p2Wmbx1Hs"
playlist = pafy.get_playlist(plurl)
print(playlist['title'])

#########################################

from django.conf import settings
from youku import YoukuVideos

from youku import YoukuUpload

def main():
    file_info = {
      'title': u'Google I/O 2014',
      'tags': 'Google,IO',
      'description': 'I/O Keynote'
    }
    file = '/home/hanguokai/filename.mp4'
    youku = YoukuUpload(settings.YOUKU_CLIENT_ID, ACCESS_TOKEN, file)
    youku.upload(file_info)


# ##########################





#############################





"""
#######################################################

"""