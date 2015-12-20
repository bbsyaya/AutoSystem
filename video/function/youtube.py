# coding=utf-8
from __future__ import unicode_literals

__author__ = 'GoTop'

import youtube_upload, pafy

def get_youtube_video_id(url):

    myvid = pafy.new("http://www.youtube.com/watch?v=dQw4w9WgXc")




def list_streams(youtube):
  print "Live streams:"

  list_streams_request = youtube.liveStreams().list(
    part="id,snippet",
    mine=True,
    maxResults=50
  )

  while list_streams_request:
    list_streams_response = list_streams_request.execute()

    for stream in list_streams_response.get("items", []):
      print "%s (%s)" % (stream["snippet"]["title"], stream["id"])

    list_streams_request = youtube.liveStreams().list_next(
      list_streams_request, list_streams_response)