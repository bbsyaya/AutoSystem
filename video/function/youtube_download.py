# coding=utf-8
from __future__ import unicode_literals, absolute_import

import logging

from celery import task
from celery_once import QueueOnce
from youtube_dl.utils import ContentTooShortError

from AutoSystem.settings import YOUTUBE_DOWNLOAD_DIR, SETTING_FILE
from AutoSystem.settings import FFMPEG_LOCATION
from video.function.youtube_playlist import get_youtube_playlist_video_info
from video.function.youtube_subtitle import download_subtitle

from video.models import Video, PlaylistConfig
import youtube_dl
from video.function.file import search_keyword_in_file


def download_multi_youtube_video_main(num):
    """
    下载num个已对标题进行翻译的youtube视频
    :return:
    """
    # 选择出前num个已经翻译过标题的youtube视频
    tran_video_list = Video.objects.filter(youku__isnull=False).order_by(
        'publishedAt', 'title')[:num]

    video_filepath_list = []
    for idx, video in enumerate(tran_video_list):
        video_filepath = download_single_youtube_video_main(video.video_id)
        video_filepath_list.append(video_filepath)

        # 将下载视频的目录保存到Video
        # video.file = video_filepath
        # video.save()
    return video_filepath_list


@task(base=QueueOnce)
def download_single_youtube_video_main(video_id, max_retey=5, file_extend=
'mp4', options={}):
    """
    下载单个youtube视频，并将下载后的视频文件的目录保存到Video.file
    :param video_id:
    file_extend 根据youtube-dl的 merge_output_format规定的来选
    :return:
    """
    if search_video_file(video_id, file_extend):
        # 视频文件之前已经下载过，返回false
        return False

    video = Video.objects.get(video_id=video_id)

    # 如果没设置options，则使用默认的设置
    if options == {}:
        # 代码参考 https://github.com/rg3/youtube-dl/blob/master/README.md#embedding
        # -youtube-dl
        # 参数 https://github.com/rg3/youtube-dl/blob/master/youtube_dl/YoutubeDL
        # .py#L121-L269
        # 参考 http://willdrevo.com/downloading-youtube-and-soundcloud-audio-with
        # -python-and-pandas/
        # 支持参数列表 https://github.com/rg3/youtube-dl/blob/master/youtube_dl
        # /options.py
        options = {
            # 'format': '160+250',  # 质量最低的视频，可以节约带宽，用于测试
            # 'format': '137+140',  # 质量最高的视频，且上传到优酷有声音
            'format': 'bestvideo[ext=mp4][height <=? 1080]+bestaudio['
                      'ext=m4a]/bestvideo[height <=? 1080] +bestaudio/best['
                      'height <=? 1080] ',

            # 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[
            # ext=mp4]/best',
            # 'format': 'bestvideo+bestaudio/best',
            # 'extractaudio': True,  # only keep the audio
            # 'audioformat': "mp3",  # convert to mp3
            # You must use %(stitle)s (and not %(title)s) to insert the video
            #  title
            # in the --output template. The "s" one is sanitized for
            # filesystems.
            'outtmpl': YOUTUBE_DOWNLOAD_DIR + '%(title)s-%(id)s.%(ext)s',
            # name the file the ID of the video
            'restrictfilenames': True,
            'noplaylist': True,  # only download single song, not playlist
            'verbose': True,  # Print various debugging information
            # 'subtitleslangs': ['zh-Hans', 'en'],  # 要写成list的形式
            # 'subtitlesformat': 'srt',
            # 'writeautomaticsub': True,  # 下载字幕，这里的字幕是youtube自动生成的CC字幕
            # 'embedsubtitles': False,  # Embed subtitles in the video (only for
            # mkv and mp4 videos
            'merge_output_format': file_extend,
            'prefer_ffmpeg': True,
            'ffmpeg_location': FFMPEG_LOCATION,
            # 'progress_hooks': [my_hook],
        }

    # 如果是本地运行，则使用代理
    if SETTING_FILE == 'local':
        # 2016-3-1fork后，支持socks代理的youtube-dl时的代理设置
        # options['socksproxy'] = '127.0.0.1:8115'
        # 2016-8-28 官方支持socks5代理时的设置
        options['proxy'] = 'socks5://127.0.0.1:8115/'

    with youtube_dl.YoutubeDL(options) as ydl:
        # youtube_url = video.youtube_url
        n = 0
        try:
            # 用设置成list的形式
            ydl.download([video.youtube_url])
        except ContentTooShortError:
            if n + 1 < max_retey:
                ydl.download([video.youtube_url])
            else:
                return False

    video_filepath = search_video_file(video_id, file_extend)

    if video_filepath:
        logger = logging.getLogger(__name__)
        logger.info("下载视频成功，视频地址为", video_filepath)

    return video_filepath


def search_video_file(video_id, file_extend):
    # 要自己查看下载目录下是否有相关video id的视频、字幕文件
    # 入存在并将视频文件的地址保存到对应的字段
    video = Video.objects.get(video_id=video_id)

    video_filepath = search_keyword_in_file(dir=YOUTUBE_DOWNLOAD_DIR,
                                            keyword=video.video_id,
                                            extend=file_extend)
    # 只能查找到一个这样的文件才对
    if (video_filepath.__len__()) == 1:
        # 从list中把唯一的一个数据pop出来
        video.file = video_filepath.pop()
        video.save()
        return video_filepath
    else:
        # 找到多个文件，暂时返回False
        return False


def download_playlist_video(num):
    """
    下载config model中设置好的youtube playlist中的num个视频，并上传到优酷，设置其playlist
    :param num:
    :return:
    """
    playlist_config_list = PlaylistConfig.objects.filter(is_enable=True)
    result_list = []
    for playlist_config in playlist_config_list:
        # 如果设置了需要下载的youtube playlist，则获取该playlist下的video id，下载
        if playlist_config.youtube_playlist.playlist_id:
            # 获取youtube_playlist中的视频的video_id
            result = get_youtube_playlist_video_info(
                youtube_playlist_id=playlist_config.youtube_playlist
                    .playlist_id, max_results=int(num))
            if result:
                video_info_list = result
                text = 'YouTube Playlist' + \
                       playlist_config.youtube_playlist.playlist_id + '的视频已保存'
                download_num = 0
                upload_num = 0
                # 下载该playlist中的视频
                for video_info in video_info_list:
                    video_id = video_info['video_id']
                    video = Video.objects.get(video_id=video_id)
                    # 如果该视频未下载，则下载视频文件和字幕文件
                    if video.is_download == False:
                        download_single_youtube_video_main.si(video_id,
                                                           max_retey=5,
                                                           file_extend='mp4')
                        #download_subtitle.si(video_id)

                        download_num = download_num + 1
                        if download_num <= num:
                            break
            else:
                video_list = []
                text = '获取youtube playlist的视频信息失败'
    return result_list
