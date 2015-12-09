# coding=utf-8
from __future__ import unicode_literals

__author__ = 'GoTop'


import youtube_upload, pafy

url = "https://www.youtube.com/watch?v=bMt47wvK6u0"

video = pafy.new(url)

print(video.title)


plurl = "https://www.youtube.com/playlist?list=PLNWIWf8IRkr9k-2nkMxb08Q2p2Wmbx1Hs"
playlist = pafy.get_playlist(plurl)
print(playlist['title'])
