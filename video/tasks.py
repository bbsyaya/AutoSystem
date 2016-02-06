# coding=utf-8
from __future__ import unicode_literals, absolute_import

# from AutoSystem.celery import app
#
# __author__ = 'GoTop'
#
#
# @app.task
# def add(x, y):
#     return x + y



from celery import task

from video.function.subtitle import merge_video_subtitle, add_subtitle_to_video_process
from video.function.video import download_upload_video
from video.models import Video


@task
def add(x, y):
    return x + y


def auto_process(num):
    """
    定期使用celery执行该命令，将下载、设置、上传视频等工作分配到worker
    不需要等待下载和上传完成
    :return:
    """
    tran_video_list = Video.set_youku.order_by('publishedAt', 'title')[:num]
    for idx, video in enumerate(tran_video_list):
        download_upload_video(video.video_id)





