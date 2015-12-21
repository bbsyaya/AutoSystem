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
    youtube = get_authenticated_service(request)
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


def my_subscription_view(request):
    """
    获取订阅我的频道的人的信息
    同一个google账号有两个用户名的，选择不同的用户名，返回的订阅信息也不一样
    :param request:
    :return:
    """
    youtube = get_authenticated_service(request)
    response = youtube.subscriptions().list(part='snippet',
                                            mine=True,
                                            maxResults=10).execute()
    subscriptions_list = []

    for result in response.get("items", []):
        subscriptions_list.append(result['snippet']["title"])
    return render_to_response('result.html',
                              {'list': subscriptions_list,
                               'text': response["pageInfo"]["totalResults"]})


def my_youtube_homepage_view(request, max_results):
    """
    获取认证用户的youtube 首页视频信息
    https://developers.google.com/youtube/v3/docs/activities/list#errors
    :param request:
    :return:
    """
    youtube = get_authenticated_service(request)
    response = youtube.activities().list(part='snippet',
                                         home=True,
                                         maxResults=max_results).execute()
    video_list = []

    for result in response.get("items", []):
        video_list.append(result['snippet']["title"])
    return render_to_response('result.html',
                              {'list': video_list})


def my_watchlater_lists_view(request, max_results):
    """
    获取认证用户的watchlater列表

    参考： https://developers.google.com/youtube/v3/docs/playlistItems/list#try-it
    :param request:
    :param max_results:
    :return:
    """
    youtube = get_authenticated_service(request)

    # Retrieve the contentDetails part of the channel resource for the
    # authenticated user's channel.
    channels_response = youtube.channels().list(
        mine=True,
        part="contentDetails"
    ).execute()

    for channel in channels_response["items"]:
        # From the API response, extract the playlist ID that identifies the list
        # of videos uploaded to the authenticated user's channel.
        watchLater_list_id = channel["contentDetails"]["relatedPlaylists"]["watchLater"]

        # Retrieve the list of watchLater videos in the authenticated user's channel.
        playlistitems_list_request = youtube.playlistItems().list(
            playlistId=watchLater_list_id,
            part="snippet",
            maxResults=50
        )

        while playlistitems_list_request:
            playlistitems_list_response = playlistitems_list_request.execute()

            # Print information about each video.
            for playlist_item in playlistitems_list_response["items"]:
                title = playlist_item["snippet"]["title"]
                video_id = playlist_item["snippet"]["resourceId"]["videoId"]
                print "%s (%s)" % (title, video_id)

        playlistitems_list_request = youtube.playlistItems().list_next(
            playlistitems_list_request, playlistitems_list_response)

        return render_to_response('result.html',
                              {'list': playlistitems_list_response})
