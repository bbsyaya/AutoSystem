# coding=utf-8
from __future__ import unicode_literals, absolute_import

import logging
import os
from celery import task

from AutoSystem.settings import YOUTUBE_DOWNLOAD_DIR
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

@task
def clean_media_directory(max_size, delete_file_num = 5):
    """
    查看 YOUTUBE_DOWNLOAD_DIR 目录的大小
    如果超过max_size则删除num个就的视频文件

    :param max_size: 10m 表示为 10 * 1024 * 1024， 单位为byte
    :param num:
    :return:
    """
    from django.conf import settings
    size = get_size(YOUTUBE_DOWNLOAD_DIR)

    if size > max_size:
        last_video = Video.downloaded.order_by('-publishedAt')[:delete_file_num]
        for video in last_video:
            print(video.video_id)
            video.delete_associate_video()
            logger = logging.getLogger(__name__)
            logger.info("删除video相关文件，video id为" + video.video_id + ",title为"
                        + video.title )
        # 循环执行本函数，直至size小于max_size
        # 测试期间先注释掉,否则会删掉很多视频
        clean_media_directory(max_size, num)

    return True

