# coding=utf-8
from __future__ import unicode_literals

import httplib2
from django.shortcuts import render, render_to_response
# Create your views here.
from django.template import RequestContext

from oauth2_authentication.function.google_oauth2_server_to_server import \
    get_authenticated_service_s2s
from video.models import Video
from oauth2_authentication.views import get_authenticated_service


def search_view(request, q, max_results):
    """
    在youtube上搜索关键字q，返回结果数设置为max_results

    :param request:
    :param q:
    :param max_results:
    :return:
    """
    #youtube = get_authenticated_service(request.user)
    youtube = get_authenticated_service_s2s()
    search_response = youtube.search().list(
        q=q,
        part="id,snippet",
        maxResults=max_results
    ).execute()

    videos = []

    channels = []
    playlists = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                       search_result["id"]["videoId"]))
        elif search_result["id"]["kind"] == "youtube#channel":
            channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                         search_result["id"]["channelId"]))
        elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                          search_result["id"]["playlistId"]))

    return render_to_response('result.html', {'list': videos})


def my_homepage_subscription_view(request, max_results):
    """
    获取认证用户的youtube首页显示的订阅频道信息,显示出来，但是不保存
    https://developers.google.com/youtube/v3/docs/activities/list#errors
    :param request:
    :return:
    """
    #youtube = get_authenticated_service(request.user)
    youtube = get_authenticated_service_s2s()

    if youtube:
        # 如果youtube.activities().list().execute(http=myhttp)使用以下代理则会提示错误:
        # "Daily Limit for Unauthenticated Use Exceeded. Continued use
        # requires signup."
        # myproxy = httplib2.ProxyInfo(
        #     proxy_type=httplib2.socks.PROXY_TYPE_SOCKS5,
        #     proxy_host='127.0.0.1', proxy_port=8115)
        # myhttp = httplib2.Http(proxy_info=myproxy)

        # home: This parameter can only be used in a properly authorized
        # request.
        #  Set this
        # parameter's value to true to retrieve the activity feed that
        # displays on
        # the YouTube home page for the currently authenticated user.
        response = youtube.activities().list(part='snippet',
                                             home=True,
                                             maxResults=max_results).execute()
        homepage_subscription_list = []
    else:
        return render_to_response('result.html',
                                  {'text': '获取google youtube服务失败，未能查询到结果'})

    for result in response.get("items", []):
        if result['snippet']["type"] == 'upload':
            homepage_subscription_list.append(result['snippet']["title"])
        else:
            # https://developers.google.com/youtube/v3/docs/activities
            # https://developers.google.com/youtube/v3/docs/activities
            # #snippet.type
            # 有的type没有title
            continue
    return render_to_response('result.html',
                              {'list': homepage_subscription_list})


def my_watchlater_lists_view(request, max_results):
    """
    获取认证用户的watchlater列表

    参考： https://developers.google.com/youtube/v3/docs/playlistItems/list#try-it
    :param request:
    :param max_results:
    :return:
    """
    #youtube = get_authenticated_service(request.user)
    youtube = get_authenticated_service_s2s()

    myproxy = httplib2.ProxyInfo(proxy_type=httplib2.socks.PROXY_TYPE_SOCKS5,
                                 proxy_host='127.0.0.1', proxy_port=8115)
    myhttp = httplib2.Http(proxy_info=myproxy)

    # Retrieve the contentDetails part of the channel resource for the
    # authenticated user's channel.
    # 通过channels查询认证用户的contentDetails里的relatedPlaylists的watchLater
    channels_response = youtube.channels().list(
        mine=True,
        part="contentDetails"
    ).execute(http=myhttp)

    for channel in channels_response["items"]:
        # From the API response, extract the playlist ID that identifies the
        # list
        # of videos uploaded to the authenticated user's channel.
        watchLater_list_id = channel["contentDetails"]["relatedPlaylists"][
            "watchLater"]

        # Retrieve the list of watchLater videos in the authenticated user's
        # channel.
        # fields 的设置参考 https://developers.google.com/youtube/v3/getting
        # -started#partial
        playlistitems_list_request = youtube.playlistItems().list(
            playlistId=watchLater_list_id,
            part="snippet",
            maxResults=max_results,
            fields="items(id,snippet/title)"
        )

        # 参考 http://stackoverflow.com/a/31795605/1314124
        res = playlistitems_list_request.execute()
        nextPageToken = res.get('nextPageToken')
        while ('nextPageToken' in res):
            nextPage = youtube.playlistItems().list(
                part="snippet",
                playlistId=watchLater_list_id,
                maxResults=max_results,
                pageToken=nextPageToken
            ).execute()
            res['items'] = res['items'] + nextPage['items']

            if 'nextPageToken' not in nextPage:
                res.pop('nextPageToken', None)
            else:
                nextPageToken = nextPage['nextPageToken']

        return render_to_response('result.html',
                                  {'list': res['items']})
