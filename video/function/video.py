# coding=utf-8
from __future__ import unicode_literals, absolute_import

from video.function.subtitle import merge_video_subtitle, \
    add_subtitle_to_video_process, \
    srt_to_ass_process, merge_sub_edit_style
from video.function.youku import set_youku_category_local, youku_upload
from video.function.youtube_download import download_single_youtube_video_main
from video.function.youtube_subsription import get_subscription_update_video
from video.function.youtube_subtitle import download_subtitle
from video.libs.subtitle import edit_two_lang_style, srt_to_ass
from video.models import Video

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


def download_upload_video(video_id):
    """
    下载youtube视频和中英字幕，合并字幕到视频，设置优酷目录，然后上传到优酷
    :param video_id:
    :return:
    """
    download_single_youtube_video_main(video_id)
    download_subtitle(video_id)

    merge_sub_edit_style(video_id)

    # 将字幕添加到视频上
    add_subtitle_to_video_process(video_id, sub_lang_type='zh-Hans_en')

    video = Video.objects.get(pk=video_id)
    set_youku_category_local(video.youku.id)
    youku_upload(video.youku.id)
