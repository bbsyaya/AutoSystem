# coding=utf-8
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response

# Create your views here.

from oauth2_authentication.views import  get_authenticated_service

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

    return render_to_response('result.html', {'list': playlists})