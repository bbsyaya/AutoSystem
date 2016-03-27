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
from video.function.subtitle import merge_video_subtitle, \
    add_subtitle_to_video_process, \
    merge_sub_edit_style
from video.function.video import download_upload_video
from video.function.youku import set_youku_category_local, youku_upload
from video.function.youtube_download import download_single_youtube_video_main
from video.function.youtube_subtitle import download_subtitle
from video.models import Video


@task
def add(x, y):
    return x + y


def auto_download_upload_video(num):
    """
    定期使用celery执行该命令，将下载、设置、上传视频等工作分配到worker
    不需要等待下载和上传完成
    :return:
    """
    tran_video_list = Video.need_upload_to_youku.order_by('publishedAt',
                                                          'title')[:num]
    for idx, video in enumerate(tran_video_list):
        # 下载youtube视频和中英字幕，合并字幕到视频，设置优酷目录，然后上传到优酷

        # download_single_youtube_video_main.s(video.video_id).delay()
        #
        # download_subtitle.s(video.video_id).delay()
        #
        # merge_sub_edit_style(video.video_id)
        #
        # # 将字幕添加到视频上
        # add_subtitle_to_video_process.s(video.video_id,
        #                                 sub_lang_type='zh-Hans_en').delay()
        #
        # set_youku_category_local(video.youku.id)
        #
        # youku_upload.s(video.youku.id).delay()

        download_video_task = download_single_youtube_video_main.si(
            video.video_id)
        download_subtitle_task = download_subtitle.si(video.video_id)
        # merge_sub_task = merge_sub_edit_style.si(video.video_id)
        add_sub_to_video_task = add_subtitle_to_video_process.si(video.video_id,
                                                                 sub_lang_type='zh-Hans_en')

        youku_upload_task = youku_upload.si(video.youku.id)

        # 将subtask chain起来执行
        (download_video_task | download_subtitle_task
         | youku_upload_task).apply_async(retry=True,
                                          retry_policy={
                                              'max_retries': 10,
                                              'interval_start': 0,
                                              'interval_step': 0.2,
                                              'interval_max': 0.2,
                                          }
                                          )


def get_info():
    pass


@task
def add_sub():
    s = add.s(2, 2).delay()
    print(s)


if __name__ == '__main__':
    import os
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoSystem.settings")
    django.setup()

    auto_download_upload_video(10)
