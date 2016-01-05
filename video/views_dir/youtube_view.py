# coding=utf-8
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from video.function.youtube import download_multi_youtube_video_main, download_single_youtube_video_main
from video.models import Video, YT_channel
from oauth2_authentication.views import get_authenticated_service


def get_subscription_update_video_view(request, max_results):
    """
    获取认证用户的youtube首页显示的订阅频道的视频信息，保存到本地数据库
    https://developers.google.com/youtube/v3/docs/activities/list#errors
    :param request:
    :return:
    """
    youtube = get_authenticated_service(request)

    # home: This parameter can only be used in a properly authorized request. Set this
    # parameter's value to true to retrieve the activity feed that displays on
    # the YouTube home page for the currently authenticated user.
    res = youtube.activities().list(part='snippet, contentDetails',
                                    home=True,
                                    maxResults=max_results).execute()

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
        channel = YT_channel.objects.filter(channel_id=result['snippet']["channelId"]).first()
        if channel and channel.is_download:
            # 如果该视频所属的频道 is_download 属性被设置为True，才进行下载
            # todo 待测试
            if result['snippet']["type"] == 'upload':
                video = {'video_id': result['contentDetails']["upload"]["videoId"],
                         'title': result['snippet']["title"],
                         'publishedAt': result['snippet']["publishedAt"],
                         'thumbnail': result['snippet']['thumbnails']["default"]["url"]
                         }

                import datetime, dateutil.parser

                # publishedAt 为ISO 8601 (YYYY-MM-DDThh:mm:ss.sZ)格式，类似2008-09-26T01:51:42.000Z
                d = dateutil.parser.parse(video['publishedAt'])

                youtube_video, created = Video.objects.update_or_create(video_id=video['video_id'],
                                                                        defaults={'title': video['title'],
                                                                                  'publishedAt': d,
                                                                                  'thumbnail': video['thumbnail']
                                                                                  }
                                                                        )

                video_list.append(video)
            else:
                # https://developers.google.com/youtube/v3/docs/activities
                # https://developers.google.com/youtube/v3/docs/activities#snippet.type
                # 有的type没有title
                continue

    return render_to_response('result.html',
                              {'text': '以下视频已保存',
                               'dict_in_list': video_list})


def download_multi_youtube_video_view(request, num):
    download_multi_youtube_video_main(num)
    # todo 添加保存下载信息到数据库的方法
    return render_to_response('result.html',
                              {'text': '视频已下载'}
                              )


def download_single_youtube_video_view(request, video_id):
    download_single_youtube_video_main(video_id)
    # todo 添加保存下载信息到数据库的方法
    return render_to_response('result.html',
                              {'text': '视频已下载'}
                              )
