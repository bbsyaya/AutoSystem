# coding=utf-8
from __future__ import unicode_literals, absolute_import
import os

# from AutoSystem.settings import YOUTUBE_DOWNLOAD_DIR
from video.models import Video

__author__ = 'GoTop'


def search_keyword_in_file(dir, keyword, extend=None):
    """
    查找dir目录下，文件名中包含keyword，后缀为extend的文件
    :param dir:
    :param keyword:
    :param extend:
    :return:
    """
    file_list = []
    for root, subFolders, files in os.walk(dir):
        for file in files:
            if extend is not None:
                # 如果设置了要查找文件的extend
                # string.find() 返回的是查找到的文本的位置，查找不成功过则返回-1
                if file.find(keyword) != -1 and file.endswith(extend):
                    file_list.append(os.path.join(dir, file))
            else:
                # 如果没设置要查找的extend
                if file.find(keyword) != -1:
                    file_list.append(os.path.join(dir, file))

    return file_list


def get_size(start_path='.'):
    """
    获取目录的大小，返回的单位是字节
    :param start_path:
    :return:单位是字节
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def clean_media_root(max_size, num):
    """
    查看 YOUTUBE_DOWNLOAD_DIR 目录的大家
    如果超过max_size则删除num个就的视频文件

    :param max_size:
    :param num:
    :return:
    """
    from django.conf import settings
    size = get_size(settings.YOUTUBE_DOWNLOAD_DIR)

    if size > max_size:
        last_video = Video.objects.order_by('-publishedAt')[:num]
        for video in last_video:
            print(video.video_id)
            video.file.delete()

