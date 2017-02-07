# coding=utf-8
from __future__ import unicode_literals, absolute_import
from celery import task
from video.function.subtitle import merge_video_subtitle, \
    add_subtitle_to_video_process, \
    srt_to_ass_process, merge_sub_edit_style, change_vtt_to_ass_and_edit_style
from video.function.youku import set_youku_category_local, youku_upload
from video.function.youku_playlist import \
    set_youku_playlist_online_from_playlist_config
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
    # 将video_id对应的Video对象的中文vtt字幕转换为ass格式
    # 并将中文ass字幕的地址保存到subtitle_merge字段
    # 然后修改ass字幕的文字式样
    change_vtt_to_ass_and_edit_style(video_id)

    # 将字幕用软压的方式添加到视频上
    # 优酷推荐的格式未：MKV容器格式，内嵌字幕的字体最好是用黑体，SSA/SRT都支持的比较好，SUB支持的不怎么好。
    # 文本编码一般正常情况下都能识别，如果不能识别就改成ANSI
    # https://www.hi-pda.com/forum/viewthread.php?tid=1962179
    add_subtitle_to_video_process(video_id, mode=
    'soft', sub_lang_type='merge')

    # 如果该video没有对应的Youku对象，就新建一个，title就用video的英文title
    if not hasattr(video, 'youku'):
        Youku.objects.create(title=video.title, video=video)

    set_youku_category_local(video.youku.id)

    if not video.youku.youku_video_id:
        youku_video_id = youku_upload(video.youku.id)

        if  youku_video_id:
            # 在playlist_config表中，根据video_id视频所属的youtube
            # playlist对应的youku playlist
            # 设置该视频在优酷上的playlist
            set_youku_playlist_online_from_playlist_config(video_id)
    else:
        youku_video_id = False

    return (video_filepath, subtitle_fielpath_list, youku_video_id)
