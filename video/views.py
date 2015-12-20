# coding=utf-8
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from video.models import Video
from oauth2_authentication.views import get_authenticated_service


def check_video_status_view(request, url):
    """
    返回视频的状态，是否已经下载到vps，是否已经上传到b百度云等
    :param request:
    :param url:
    :return:
    """


def get_subscription_list_view(request):
    """
    获取自己账号的订阅列表
    :param request:
    :return:
    """


def get_youtube_list_video_url_view(request, list_url):
    """
    获取youtube的list里的视频链接
    :param request:
    :param list_url:
    :return:
    """


def download_video_view(request, url):
    """
    下载youtube的视频到VPS
    :param request:
    :param url:
    :return:
    """


def upload_video_to_baiduyun_view(request, video_id):
    """
    上传视频到百度云
    :param request:
    :param video_id:
    :return:
    """


def search_view(request, q, max_results):
    """
    在youtube上搜索关键字q，返回结果数设置为max_results

    :param request:
    :param q:
    :param max_results:
    :return:
    """
    service = get_authenticated_service(request)
    search_response = service.search().list(
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


def my_subscription_view(request):
    """
    获取订阅我的频道的人的信息
    :param request:
    :return:
    """
    service = get_authenticated_service(request)
    response = service.subscriptions().list(part='snippet',
                                            mine=True,
                                            maxResults=10).execute()
    subscriptions_list = []

    for result in response.get("items", []):
        subscriptions_list.append(result['snippet']["title"])
    return render_to_response('result.html',
                              {'list': subscriptions_list,
                               'text': response["pageInfo"]["totalResults"]})



