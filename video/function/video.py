# coding=utf-8
from __future__ import unicode_literals, absolute_import

from celery import task

from video.function.subtitle import merge_video_subtitle, \
    add_subtitle_to_video_process, \
    srt_to_ass_process, merge_sub_edit_style
from video.function.youku import set_youku_category_local, youku_upload
from video.function.youtube_download import download_single_youtube_video_main
from video.function.youtube_subsription import get_subscription_update_video
from video.function.youtube_subtitle import download_subtitle
from video.libs.subtitle import edit_two_lang_style
from video.models import Video, Youku

__author__ = 'GoTop'


def auto_download_upload_video():
    # 获取认证用户的youtube首页显示的订阅频道的视频信息，保存到本地数据库
    get_subscription_update_video(user='admin', max_results=50)

    # 下载视频
    # 选择出前num个已经翻译过标题的youtube视频
    num = 10
    tran_video_list = Video.set_youku.order_by('publishedAt', 'title')[:num]

    downloaded_video_list = []
    for idx, video in enumerate(tran_video_list):
        download_upload_video(video.video_id)


@task
def download_upload_video(video_id):
    """
    下载video_id为 video_id 的youtube视频和中英字幕，合并字幕到视频，设置优酷目录，然后上传到优酷
    :param video_id:
    :return:
    """
    video = Video.objects.get(pk=video_id)

    if not video.file:
        video_filepath = download_single_youtube_video_main(video_id)
    else:
        video_filepath = False

    if not video.subtitle_en:
        subtitle_fielpath_list = download_subtitle(video_id)
    else:
        subtitle_fielpath_list = []

    # merge_sub_edit_style(video_id)

    # 将字幕添加到视频上
    # 因为Linode上压制字幕到视频的时间很慢，所以先注释掉 2016-3-31
    # add_subtitle_to_video_process(video_id, sub_lang_type='zh-Hans')

    # 如果该video没有对应的Youku对象，就新建一个，title就用video的英文title
    if not hasattr(video, 'youku'):
        Youku.objects.create(title=video.title, video=video)

    set_youku_category_local(video.youku.id)

    if not video.youku.video_id:
        youku_video_id = youku_upload(video.youku.id)
    else:
        youku_video_id = False

    return (video_filepath, subtitle_fielpath_list, youku_video_id)
