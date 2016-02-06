# coding=utf-8
from __future__ import unicode_literals

from AutoSystem import settings
from AutoSystem.settings import YOUTUBE_DOWNLOAD_DIR
from video.function.subtitle import add_subtitle_to_video
from video.models import Video, YT_channel

import youtube_dl

from oauth2_authentication.views import get_authenticated_service
from video.utils.file import search_keyword_in_file

__author__ = 'GoTop'

def get_subscription_update_video(user, max_results):
    """
    获取认证用户的youtube首页显示的订阅频道的视频信息，保存到本地数据库
    https://developers.google.com/youtube/v3/docs/activities/list#errors
    :param request:
    :return:
    """
    youtube = get_authenticated_service(user)  # home: This parameter can only be used in a properly authorized request. Set this
    # parameter's value to true to retrieve the activity feed that displays on
    # the YouTube home page for the currently authenticated user.
    res = youtube.activities().list(part='snippet, contentDetails',
                                    home=True,
                                    maxResults=max_results).execute()

    # 循环获取完所有的结果
    nextPageToken = res.get('nextPageToken')
    while ('nextPageToken' in res):
        nextPage = youtube.activities().list(
                part='snippet, contentDetails',
                home=True,
                maxResults=max_results,
                pageToken=nextPageToken
        ).execute()
        res['items'] = res['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            res.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']

    # 从返回的对象里找出type为upload的
    video_list = []
    for result in res.get("items", []):
        channel = YT_channel.objects.filter(channel_id=result['snippet']["channelId"]).first()
        if channel and channel.is_download:
            # 如果该视频所属的频道 is_download 属性被设置为True，才进行下载
            # todo 待测试
            if result['snippet']["type"] == 'upload':
                video = {'video_id': result['contentDetails']["upload"]["videoId"],
                         'title': result['snippet']["title"],
                         'publishedAt': result['snippet']["publishedAt"],
                         'thumbnail': result['snippet']['thumbnails']["default"]["url"],
                         'channel': result['snippet']["channelId"]
                         }

                import datetime, dateutil.parser

                # publishedAt 为ISO 8601 (YYYY-MM-DDThh:mm:ss.sZ)格式，类似2008-09-26T01:51:42.000Z
                d = dateutil.parser.parse(video['publishedAt'])

                youtube_video, created = Video.objects.update_or_create(video_id=video['video_id'],
                                                                        defaults={'title': video['title'],
                                                                                  'publishedAt': d,
                                                                                  'thumbnail': video['thumbnail'],
                                                                                  'channel': channel
                                                                                  }
                                                                        )

                video_list.append(video)
            else:
                # https://developers.google.com/youtube/v3/docs/activities
                # https://developers.google.com/youtube/v3/docs/activities#snippet.type
                # 有的type没有title
                continue
    return video_list


def download_multi_youtube_video_main(num):
    """
    下载num个已对标题进行翻译的youtube视频
    :return:
    """
    # 选择出前num个已经翻译过标题的youtube视频
    tran_video_list = Video.objects.filter(youku__isnull=False).order_by('publishedAt', 'title')[:num]

    video_filepath_list = []
    for idx, video in enumerate(tran_video_list):
        video_filepath = download_single_youtube_video_main(video.video_id)
        video_filepath_list.append(video_filepath)

        # 将下载视频的目录保存到Video
        #video.file = video_filepath
        #video.save()
    return video_filepath_list

    # # 代码参考 https://github.com/rg3/youtube-dl/blob/master/README.md#embedding-youtube-dl
    # # 参数 https://github.com/rg3/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L121-L269
    # # 参考 http://willdrevo.com/downloading-youtube-and-soundcloud-audio-with-python-and-pandas/
    # # 支持参数列表 https://github.com/rg3/youtube-dl/blob/master/youtube_dl/options.py
    # options = {
    #     'format': '160+250',  # choice of quality
    #     # 'extractaudio': True,  # only keep the audio
    #     # 'audioformat': "mp3",  # convert to mp3
    #     'outtmpl': settings.YOUTUBE_DOWNLOAD_DIR + '\%(title)s-%(id)s.%(ext)s',  # name the file the ID of the video
    #     'noplaylist': True,  # only download single song, not playlist
    #     'verbose': True,
    #     'subtitleslangs': ['zh-Hans', 'en'],  # 要写成list的形式
    #     'writeautomaticsub': True,
    #     'embedsubtitles': True,
    #     'merge_output_format': 'mkv',
    #     'prefer_ffmpeg': True,
    #     'ffmpeg_location': "E:\\Program Files\\ffmpeg\\bin"
    #     # 'progress_hooks': [my_hook],
    # }
    #
    # video_filepath_list = []
    # for idx, video in enumerate(tran_video_list):
    #     with youtube_dl.YoutubeDL(options) as ydl:
    #         # youtube_url = video.youtube_url
    #         # 用设置成list的形式
    #         ydl.download([video.youtube_url])
    #
    #         # youtube-dl下载成功后并不会返回下载视频文件的信息
    #         # todo 所以要自己查看下载目录下是否有相关video id的视频，以此来判断是否下载成功
    #         # 并将视频文件的地址保存到对应的字段
    #         video_filepath = search_keyword_in_file(dir=settings.YOUTUBE_DOWNLOAD_DIR,
    #                                                 keyword=video.video_id,
    #                                                 extend=options.get('merge_output_format', None))
    #         if (video_filepath.__len__()) == 1:
    #             # 从list中把唯一的一个数据pop出来
    #             video_filepath = video_filepath.pop()
    #             video_filepath_list.append(video_filepath)
    #             video.file = video_filepath
    #             video.save()
    #     # 控制for循环的次数，从而控制下载的视频数
    #     # 参考 http://stackoverflow.com/questions/3162271/get-loop-count-inside-a-python-for-loop
    #     if idx > num:
    #         break
    #
    # # todo 返回成功下的的视频列表
    # return video_filepath_list


def download_single_youtube_video_main(video_id):
    """
    下载单个youtube视频，并将下载后的视频文件的目录保存到Video.file
    :param video_id:
    :return:
    """
    video = Video.objects.get(video_id=video_id)

    # 代码参考 https://github.com/rg3/youtube-dl/blob/master/README.md#embedding-youtube-dl
    # 参数 https://github.com/rg3/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L121-L269
    # 参考 http://willdrevo.com/downloading-youtube-and-soundcloud-audio-with-python-and-pandas/
    # 支持参数列表 https://github.com/rg3/youtube-dl/blob/master/youtube_dl/options.py
    options = {
        'format': '160+250',  # choice of quality
        # 'extractaudio': True,  # only keep the audio
        # 'audioformat': "mp3",  # convert to mp3
        'outtmpl': settings.YOUTUBE_DOWNLOAD_DIR + '\%(title)s-%(id)s.%(ext)s',  # name the file the ID of the video
        'noplaylist': True,  # only download single song, not playlist
        'verbose': True,
        'subtitleslangs': ['zh-Hans', 'en'],  # 要写成list的形式
        'subtitlesformat': 'srt',
        'writeautomaticsub': True,  # 下载字幕，这里的字幕是youtube自动生成的CC字幕
        'embedsubtitles': True,
        'merge_output_format': 'mkv',
        'prefer_ffmpeg': True,
        'ffmpeg_location': "E:\\Program Files\\ffmpeg\\bin"
        # 'progress_hooks': [my_hook],
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        # youtube_url = video.youtube_url
        # 用设置成list的形式
        ydl.download([video.youtube_url])

        # youtube-dl下载成功后并不会返回下载视频文件的信息
        # todo 所以要自己查看下载目录下是否有相关video id的视频，以此来判断是否下载成功
        # 并将视频文件的地址保存到对应的字段
        video_filepath = search_keyword_in_file(dir=settings.YOUTUBE_DOWNLOAD_DIR,
                                                keyword=video.video_id,
                                                extend=options.get('merge_output_format', None))
        # 只能查找到一个这样的文件才对
        if (video_filepath.__len__()) == 1:
            # 从list中把唯一的一个数据pop出来
            video.file = video_filepath.pop()

        # 只适用于subtitlesformat设置为srt或ass的情况，设置为best则失效
        # 字幕名称格式 LG K10 and K7 hands-on-_9coAtC2PZI.en.srt
        subtitle_en_filepath = search_keyword_in_file(dir=settings.YOUTUBE_DOWNLOAD_DIR,
                                                      keyword=video.video_id + ".en",
                                                      extend=options.get('subtitlesformat', None))
        if (subtitle_en_filepath.__len__()) == 1:
            # 从list中把唯一的一个数据pop出来
            video.subtitle_en = subtitle_en_filepath.pop()

        subtitle_cn_filepath = search_keyword_in_file(dir=settings.YOUTUBE_DOWNLOAD_DIR,
                                                      keyword=video.video_id + ".zh-Hans",
                                                      extend=options.get('subtitlesformat', None))
        if (subtitle_cn_filepath.__len__()) == 1:
            # 从list中把唯一的一个数据pop出来
            video.subtitle_cn = subtitle_cn_filepath.pop()

        video.save()
    return video_filepath



