# coding=utf-8
from __future__ import unicode_literals, absolute_import

from oauth2_authentication.function.google_oauth2_server_to_server import \
    get_authenticated_service_s2s
from video.models import Video, YouTubeChannel
from oauth2_authentication.views import get_authenticated_service

__author__ = 'GoTop'


def get_subscription_update_video(user, max_results):
    """
    获取认证用户的youtube首页显示的订阅频道的视频信息，保存到本地数据库
    https://developers.google.com/youtube/v3/docs/activities/list#errors
    :param request:
    max_results：最大为50
    :return:
    """
    #youtube = get_authenticated_service(user)
    youtube = get_authenticated_service_s2s()
    # home: This parameter can only be used in a properly
    # authorized request. Set this
    # parameter's value to true to retrieve the activity feed that displays on
    # the YouTube home page for the currently authenticated user.

    # home=True 获取登陆用户的首页推荐视频
    # mine=True 获取登陆用户进行like，upload等操作的视频
    # home和mine 不能同时为True，否者会提示错误
    if youtube:
        res = youtube.activities().list(
        part='snippet, contentDetails',
            home=True,
            maxResults=max_results).execute()
    else:
        return False

    # 循环获取完所有的结果
    nextPageToken = res.get('nextPageToken')
    while ('nextPageToken' in res):
        nextPage = youtube.activities().list(
            part='snippet, contentDetails',
            home=True,
            maxResults=max_results,
            pageToken=nextPageToken
        ).execute()
        res['items'] = res['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            res.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']

    # 从返回的对象里找出type为upload的
    video_list = []
    for result in res.get("items", []):
        # 查询看该视频所属的channel是否保存到了数据库中
        channel = YouTubeChannel.objects.filter(
            channel_id=result['snippet']["channelId"]).first()
        #如果视频所属的channel保存在YouTubeChannel中，并且is_download属性为true
        if channel and channel.is_download:
            # 如果该视频所属的频道 is_download 属性被设置为True，才进行下载
            # todo 待测试
            if result['snippet']["type"] == 'upload':
                video = {
                    'video_id': result['contentDetails']["upload"]["videoId"],
                    'title': result['snippet']["title"],
                    'publishedAt': result['snippet']["publishedAt"],
                    'thumbnail': result['snippet']['thumbnails']["default"][
                        "url"],
                    'channel': result['snippet']["channelId"]
                }

                import datetime, dateutil.parser

                # publishedAt 为ISO 8601 (
                # YYYY-MM-DDThh:mm:ss.sZ)格式，类似2008-09-26T01:51:42.000Z
                d = dateutil.parser.parse(video['publishedAt'])

                youtube_video, created = Video.objects.update_or_create(
                    video_id=video['video_id'],
                    defaults={'title': video['title'],
                              'publishedAt': d,
                              'thumbnail': video['thumbnail'],
                              'channel': channel
                              }
                )

                video_list.append(video)
            else:
                # https://developers.google.com/youtube/v3/docs/activities
                # https://developers.google.com/youtube/v3/docs/activities
                # #snippet.type
                # 有的type没有title
                continue
    return video_list
