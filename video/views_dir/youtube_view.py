# coding=utf-8
from __future__ import unicode_literals, absolute_import
from django.shortcuts import render, render_to_response
# Create your views here.

from video.function.youtube_download import download_multi_youtube_video_main
from video.function.youtube_download import download_single_youtube_video_main
from video.function.youtube_video_info import get_multi_youtube_video_info
from video.function.youtube_subtitle import download_subtitle
from video.function.youtube_subsription import get_subscription_update_video
from video.models import Video


def get_subscription_update_video_view(request, max_results):
    """
    获取认证用户的youtube首页显示的订阅频道的视频信息，保存到本地数据库
    https://developers.google.com/youtube/v3/docs/activities/list#errors
    :param request:
    max_results: 最大为50
    :return:
    """
    result = get_subscription_update_video(request.user, max_results)

    if result:
        video_list = result
        text = '以下视频已保存'
    else:
        video_list = []
        text = '获取youtube视频信息失败'

    return render_to_response('result.html',
                              {'text': text,
                               'dict_in_list': video_list})


def download_multi_youtube_video_view(request, num):
    download_multi_youtube_video_main(num)
    # todo 添加保存下载信息到数据库的方法
    return render_to_response('result.html',
                              {'text': '视频已下载'}
                              )


def download_single_youtube_video_view(request, video_id):
    download_single_youtube_video_main(video_id, 'mkv')
    # todo 添加保存下载信息到数据库的方法
    return render_to_response('result.html',
                              {'text': '视频已下载'}
                              )


def download_subtitle_view(request, video_id):
    result = download_subtitle(video_id, subtitlesformat='vtt', max_retey=3)
    if result is False:
        result = []
    return render_to_response('result.html',
                              {'list': result}
                              )


def get_multi_youtube_video_info_view(request):
    youtube_video_id_list = get_multi_youtube_video_info()
    return render_to_response('result.html',
                              {'list': youtube_video_id_list}
                              )


def auto_youtube_download_view(request, num):
    """
    自动下载num个设置了youku title属性的video视频到本地
    :return:
    """
    # 按publishedAt 倒序查找前num个，file 属性是null（即没下载过视频到本地），
    # 对应的youku.title不为''（设置过中文title）的video视频
    video_list = Video.objects.filter(file='').filter(
        youku__title__isnull=False).order_by('-publishedAt')[
                 :num]
    youtube_downlaoded_list = []
    for video in video_list:
        youtube_downlaoded = download_single_youtube_video_main(video.video_id)
        youtube_downlaoded_list.append(youtube_downlaoded.title)

    return render_to_response('result.html', {'list': youtube_downlaoded_list})
