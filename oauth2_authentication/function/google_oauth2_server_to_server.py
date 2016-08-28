# coding=utf-8
from __future__ import unicode_literals, absolute_import

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

__author__ = 'GoTop'

from AutoSystem.settings import SCOPES, YOUTUBE_API_SERVICE_NAME, \
    YOUTUBE_API_VERSION

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'G:\Python\Project\AutoSystem\AutoSystem\settings\AutoSystem-c7e714b350c6'
    '.json',
    SCOPES)
myproxy = httplib2.ProxyInfo(
    proxy_type=httplib2.socks.PROXY_TYPE_HTTP,
    proxy_host='127.0.0.1', proxy_port=8118)

proxy_http = httplib2.Http(proxy_info=myproxy)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                credentials=credentials, http=proxy_http)

if youtube:
    res = youtube.playlistItems().list(
        part='snippet, contentDetails',
        playlistId='PLNWIWf8IRkr_gX4fOQndZOIeuvofx4L6z',
        maxResults=50).execute()

    # 将该playlist包含的视频数量保存到YouTubePlaylist中
    # if res:
    #     video_num = res['pageInfo']['totalResults']
    #     playlist.video_num = video_num
    #     playlist.save(update_fields=['video_num'])



    # 循环获取完所有的结果
    nextPageToken = res.get('nextPageToken')
    while ('nextPageToken' in res):
        nextPage = youtube.playlistItems().list(
            part='snippet, contentDetails',
            playlistId='PLNWIWf8IRkr_gX4fOQndZOIeuvofx4L6z',
            maxResults=50,
            pageToken=nextPageToken
        ).execute()

        res['items'] = res['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            res.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']

    for result in res.get("items", []):
        print(result)
