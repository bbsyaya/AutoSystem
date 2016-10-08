# coding=utf-8
from __future__ import unicode_literals, absolute_import
import json
import isodate as isodate

from oauth2_authentication.function.google_oauth2_server_to_server import \
    get_authenticated_service_s2s
from video.models import Video
import youtube_dl
from oauth2_authentication.views import get_authenticated_service

__author__ = 'GoTop'


def get_video_info(video_id):
    video = Video.objects.get(video_id=video_id)
    options = {
        # name the file the ID of the video
        # 'format': 'bestvideo+bestaudio/best',
        'verbose': True,  # Print various debugging information
        'skip_download': True,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(video.youtube_url, download=False)

        from pprint import pprint
        pprint(info_dict)

        video.view_count = info_dict['view_count']
        video.like_count = info_dict['like_count']
        video.tags = json.dumps(info_dict['tags'])  # 将list转成json的格式保存到数据库中
        video.duration = info_dict['duration']
        video.save()


def get_multi_youtube_video_info():
    """
    一次获取max_results个保存在Video model中的youtube视频的时长，播放数等额外信息
    :param user:
    :param max_results: <50
    :return:
    """
    video_list = Video.need_get_video_info.order_by('-publishedAt')[:50]
    video_id_list = []
    for video in video_list:
        video_id_list.append(video.video_id)

    video_id_string = ', '.join(video_id_list)
    #youtube = get_authenticated_service(user)
    youtube = get_authenticated_service_s2s()
    # https://developers.google.com/youtube/v3/docs/videos/list
    res = youtube.videos().list(
        part="contentDetails, snippet, statistics",
        id=video_id_string
    ).execute()

    # 循环获取完所有的结果
    nextPageToken = res.get('nextPageToken')
    while ('nextPageToken' in res):
        nextPage = youtube.videos().list(
            part="contentDetails, snippet, statistics",
            id=video_id_string,
            pageToken=nextPageToken
        ).execute()
        res['items'] = res['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            res.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']

    # 从返回的对象里找出type为upload的
    youtube_video_id_list = []
    for result in res.get("items", []):
        video = Video.objects.get(pk=result['id'])

        # 某些youtube视频没有tags
        # 比如 https://www.youtube.com/watch?v=_Po6DWVPbmQ
        # 如果没有tags,则返回'',这样json.dumps(tags_list)的结果就是''
        # video model的tags是TEXTField，''就是其空值
        tags_list = result['snippet'].get('tags', '')
        video.tags = json.dumps(tags_list)

        # https://docs.djangoproject.com/en/1.6/ref/models/instances
        # /#specifying-which-fields-to-save

        video.view_count = result['statistics'].get('viewCount', 0)
        # 某些youtube视频没有likeCount
        # 比如 https://www.youtube.com/watch?v=YiTAEQNFI4A
        video.like_count = result['statistics'].get('likeCount', 0)
        # 将list转成json的格式保存到数据库中

        # http://stackoverflow.com/a/16743442/1314124
        duration = isodate.parse_duration(result['contentDetails']['duration'])
        video.duration = duration.total_seconds()
        video.save(
            update_fields=['view_count', 'like_count', 'tags', 'duration'])
        youtube_video_id_list.append(result['id'])
    return youtube_video_id_list
