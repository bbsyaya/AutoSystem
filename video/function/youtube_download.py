# coding=utf-8
from __future__ import unicode_literals, absolute_import
from AutoSystem.settings.base import YOUTUBE_DOWNLOAD_DIR
from AutoSystem.settings.base import DEBUG
from video.models import Video
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


def download_single_youtube_video_main(video_id):
    """
    下载单个youtube视频，并将下载后的视频文件的目录保存到Video.file
    :param video_id:
    :return:
    """
    video = Video.objects.get(video_id=video_id)

    # 代码参考 https://github.com/rg3/youtube-dl/blob/master/README.md#embedding
    # -youtube-dl
    # 参数 https://github.com/rg3/youtube-dl/blob/master/youtube_dl/YoutubeDL
    # .py#L121-L269
    # 参考 http://willdrevo.com/downloading-youtube-and-soundcloud-audio-with
    # -python-and-pandas/
    # 支持参数列表 https://github.com/rg3/youtube-dl/blob/master/youtube_dl/options.py
    options = {
        # 'format': '160+250',  # 质量最低的视频，可以节约带宽，用于测试
        # 'format': '137+140',  # 质量最高的视频，且上传到优酷有声音

        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        # 'format': 'bestvideo+bestaudio/best',
        # 'extractaudio': True,  # only keep the audio
        # 'audioformat': "mp3",  # convert to mp3
        'outtmpl': YOUTUBE_DOWNLOAD_DIR + '\%(title)s-%(id)s.%(ext)s',
        # name the file the ID of the video
        'restrictfilenames': True,
        'noplaylist': True,  # only download single song, not playlist
        'verbose': True,  # Print various debugging information
        # 'subtitleslangs': ['zh-Hans', 'en'],  # 要写成list的形式
        # 'subtitlesformat': 'srt',
        # 'writeautomaticsub': True,  # 下载字幕，这里的字幕是youtube自动生成的CC字幕
        # 'embedsubtitles': False,  # Embed subtitles in the video (only for
        # mkv and mp4 videos
        'merge_output_format': 'mkv',
        'prefer_ffmpeg': True,
        'ffmpeg_location': "E:\\Program Files\\ffmpeg\\bin",
        # 'progress_hooks': [my_hook],
        'socksproxy': '127.0.0.1:8115'
    }

    #如果是本地debug状态则使用代理
    if DEBUG == True:
        options['socksproxy'] = '127.0.0.1:8115'

    with youtube_dl.YoutubeDL(options) as ydl:
        # youtube_url = video.youtube_url
        # 用设置成list的形式
        ydl.download([video.youtube_url])

        # youtube-dl下载成功后并不会返回下载视频文件的信息
        # 要自己查看下载目录下是否有相关video id的视频，以此来判断是否下载成功
        # 并将视频文件的地址保存到对应的字段
        video_filepath = search_keyword_in_file(dir=YOUTUBE_DOWNLOAD_DIR,
                                                keyword=video.video_id,
                                                extend=options.get(
                                                    'merge_output_format',
                                                    None))
        # 只能查找到一个这样的文件才对
        if (video_filepath.__len__()) == 1:
            # 从list中把唯一的一个数据pop出来
            video.file = video_filepath.pop()

        video.save()
    return video_filepath
