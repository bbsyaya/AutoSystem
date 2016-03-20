# coding=utf-8
from __future__ import unicode_literals, absolute_import
from django.shortcuts import render, render_to_response

from oauth2_authentication.views import get_authenticated_service
from video.models import YT_channel

__author__ = 'GoTop'


def get_my_subscription_view(request):
    """
    获取认证用户订阅的频道的信息
    同一个google账号有两个用户名的，选择不同的用户名，返回的订阅信息也不一样
    :param request:
    :return:
    """
    max_results = 10
    youtube = get_authenticated_service(request.user)
    res = youtube.subscriptions().list(part='snippet',
                                       mine=True,
                                       maxResults=max_results).execute()
    # 循环获取完所有的结果
    nextPageToken = res.get('nextPageToken')
    while ('nextPageToken' in res):
        nextPage = youtube.subscriptions().list(
                part='snippet',
                mine=True,
                maxResults=max_results,
                pageToken=nextPageToken
        ).execute()
        res['items'] = res['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            res.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']

    subscriptions_list = []
    for result in res.get("items", []):
        subscriptions_list.append(result['snippet'])

    for subscription in subscriptions_list:
        channel, created = YT_channel.objects.update_or_create(
                channel_id=subscription['resourceId']['channelId'],
                defaults={'title': subscription['title'],
                          'description': subscription['description'],
                          'thumbnail': subscription['thumbnails']['default']['url']
                          }
        )

    return render_to_response('result.html',
                              {'list': subscriptions_list,
                               'text': res["pageInfo"]["totalResults"]})
