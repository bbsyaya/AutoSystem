# coding=utf-8
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from video.models import Video


def check_video_status_view(request, url):
    """
    返回视频的状态，是否已经下载到vps，是否已经上传到b百度云等
    :param request:
    :param url:
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
