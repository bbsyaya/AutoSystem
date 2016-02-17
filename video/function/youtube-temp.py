# coding=utf-8
from __future__ import unicode_literals, absolute_import
import json
import isodate as isodate
import simplejson
from AutoSystem import settings
from AutoSystem.settings.base import YOUTUBE_DOWNLOAD_DIR
from video.function.subtitle import add_subtitle_to_video
from video.models import Video, YT_channel
import youtube_dl
from oauth2_authentication.views import get_authenticated_service
from video.function.file import search_keyword_in_file

__author__ = 'GoTop'


def get_subscription_update_video(user, max_results):
    """
    获取认证用户的youtube首页显示的订阅频道的视频信息，保存到本地数据库
    https://developers.google.com/youtube/v3/docs/activities/list#errors
    :param request:
    :return:
    """
    youtube = get_authenticated_service(
        user)  # home: This parameter can only be used in a properly
    # authorized request. Set this
    # parameter's value to true to retrieve the activity feed that displays on
    # the YouTube home page for the currently authenticated user.
    res = youtube.activities().list(
        part='snippet, contentDetails',
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
        channel = YT_channel.objects.filter(
            channel_id=result['snippet']["channelId"]).first()
        if channel and channel.is_download:
            # 如果该视频所属的频道 is_download 属性被设置为True，才进行下载
            # todo 待测试
            if result['snippet']["type"] == 'upload':
                video = {
                    'video_id': result['contentDetails']["upload"]["videoId"],
                    'title': result['snippet']["title"],
                    'publishedAt': result['snippet']["publishedAt"],
                    'thumbnail': result['snippet']['thumbnails']["default"][
                        "url"],
                    'channel': result['snippet']["channelId"]
                }

                import datetime, dateutil.parser

                # publishedAt 为ISO 8601 (
                # YYYY-MM-DDThh:mm:ss.sZ)格式，类似2008-09-26T01:51:42.000Z
                d = dateutil.parser.parse(video['publishedAt'])

                youtube_video, created = Video.objects.update_or_create(
                    video_id=video['video_id'],
                    defaults={'title': video['title'],
                              'publishedAt': d,
                              'thumbnail': video['thumbnail'],
                              'channel': channel
                              }
                )

                video_list.append(video)
            else:
                # https://developers.google.com/youtube/v3/docs/activities
                # https://developers.google.com/youtube/v3/docs/activities
                # #snippet.type
                # 有的type没有title
                continue
    return video_list


def get_multi_youtube_video_info(user):
    """
    一次获取max_results个youtube视频的时长，播放数等额外信息
    :param user:
    :param max_results: <50
    :return:
    """
    video_list = Video.need_get_video_info.order_by('-publishedAt')[:50]
    video_id_list = []
    for video in video_list:
        video_id_list.append(video.video_id)

    video_id_string = ', '.join(video_id_list)
    youtube = get_authenticated_service(user)
    # https://developers.google.com/youtube/v3/docs/videos/list
    res = youtube.videos().list(
        part="contentDetails, snippet, statistics",
        id=video_id_string
    ).execute()

    # 循环获取完所有的结果
    nextPageToken = res.get('nextPageToken')
    while ('nextPageToken' in res):
        nextPage = youtube.videos().list(
            part="contentDetails",
            id=video_list,
            pageToken=nextPageToken
        ).execute()
        res['items'] = res['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            res.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']

    # 从返回的对象里找出type为upload的
    youtube_video_id_list = []
    for result in res.get("items", []):
        video = Video.objects.get(pk=result['id'])

        # 某些youtube视频没有tags
        # 比如 https://www.youtube.com/watch?v=_Po6DWVPbmQ
        tags_list = result['snippet'].get('tags', None)
        video.tags = json.dumps(tags_list)

        # https://docs.djangoproject.com/en/1.6/ref/models/instances
        # /#specifying-which-fields-to-save

        video.view_count = result['statistics'].get('viewCount', 0)
        # 某些youtube视频没有likeCount
        # 比如 https://www.youtube.com/watch?v=YiTAEQNFI4A
        video.like_count = result['statistics'].get('likeCount', 0)
        # 将list转成json的格式保存到数据库中

        # http://stackoverflow.com/a/16743442/1314124
        duration = isodate.parse_duration(result['contentDetails']['duration'])
        video.duration = duration.total_seconds()
        video.save(
            update_fields=['view_count', 'like_count', 'tags', 'duration'])
        youtube_video_id_list.append(result['id'])
    return youtube_video_id_list


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
        video_filepath = search_keyword_in_file(dir=YOUTUBE_DOWNLOAD_DIR,
                                                keyword=video.video_id,
                                                extend=options.get(
                                                    'merge_output_format',
                                                    None))
        # 只能查找到一个这样的文件才对
        if (video_filepath.__len__()) == 1:
            # 从list中把唯一的一个数据pop出来
            video.file = video_filepath.pop()

        # 只适用于subtitlesformat设置为srt或ass的情况，设置为best则失效
        # 字幕名称格式 LG K10 and K7 hands-on-_9coAtC2PZI.en.srt
        # subtitle_en_filepath = search_keyword_in_file(dir=YOUTUBE_DOWNLOAD_DIR,
        #                                               keyword=video.video_id
        #                                                       + ".en",
        #                                               extend=options.get(
        #                                                   'subtitlesformat',
        #                                                   None))

        video.save()
    return video_filepath


def download_subtitle(video_id):
    """
    下载video的中英字幕并保存到video model中

    :param video_id:
    :return:
    """
    video = Video.objects.get(video_id=video_id)
    options = {
        'outtmpl': YOUTUBE_DOWNLOAD_DIR + '\%(title)s-%(id)s.%(ext)s',
        # name the file the ID of the video
        'verbose': True,  # Print various debugging information
        'restrictfilenames': True,
        'subtitleslangs': ['en', 'zh-Hans'],  # 要写成list的形式
        # 'convertsubtitles': 'srt',
        'subtitlesformat': 'vtt',
        'writeautomaticsub': True,  # 下载字幕，这里的字幕是youtube自动生成的CC字幕
        'skip_download': True,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video.youtube_url])

        # 只适用于subtitlesformat设置为srt或ass的情况，设置为best则失效
        # 字幕名称格式 LG K10 and K7 hands-on-_9coAtC2PZI.en.srt
        subtitle_en_filepath = search_keyword_in_file(dir=YOUTUBE_DOWNLOAD_DIR,
                                                      keyword=video.video_id
                                                              + ".en",
                                                      extend=options.get(
                                                          'subtitlesformat',
                                                          None))

        result = []
        if (subtitle_en_filepath.__len__()) == 1:
            # 从list中把唯一的一个数据pop出来
            video.subtitle_en = subtitle_en_filepath.pop()
            result.append(video.subtitle_en)

        subtitle_cn_filepath = search_keyword_in_file(dir=YOUTUBE_DOWNLOAD_DIR,
                                                      keyword=video.video_id
                                                              + ".zh-Hans",
                                                      extend=options.get(
                                                          'subtitlesformat',
                                                          None))
        if (subtitle_cn_filepath.__len__()) == 1:
            # 从list中把唯一的一个数据pop出来
            video.subtitle_cn = subtitle_cn_filepath.pop()
            result.append(video.subtitle_en)

        video.save()

    if result == []:
        result = False
    return result


def get_video_info(video_id):
    video = Video.objects.get(video_id=video_id)
    options = {
        # name the file the ID of the video
        # 'format': 'bestvideo+bestaudio/best',
        'verbose': True,  # Print various debugging information
        'skip_download': True,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(video.youtube_url, download=False)

        from pprint import pprint
        pprint(info_dict)

        video.view_count = info_dict['view_count']
        video.like_count = info_dict['like_count']
        video.tags = json.dumps(info_dict['tags'])  # 将list转成json的格式保存到数据库中
        video.duration = info_dict['duration']
        video.save()
