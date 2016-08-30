# coding=utf-8
from __future__ import unicode_literals, absolute_import
import dateutil.parser

from oauth2_authentication.function.google_oauth2_server_to_server import \
    get_authenticated_service_s2s
from oauth2_authentication.views import get_authenticated_service
from video.models import Video, YouTubeChannel, YouTubePlaylist

__author__ = 'GoTop'


def get_youtube_playlist_info(youtube_channel_id, max_results, user):
    # 获取channel中的用户自定义的youtube playlist的信息并保存到数据中
    # https://developers.google.com/youtube/v3/docs/playlists/list#parameters

    # GET https://www.googleapis.com/youtube/v3/playlists?part=snippet
    # &channelId=UCEQpJTOXGkvS1UQsdCm6lLA&key={YOUR_API_KEY}
    #youtube = get_authenticated_service(user)
    youtube = get_authenticated_service_s2s()
    if youtube:
        res = youtube.playlists().list(
            part='snippet',
            channelId=youtube_channel_id,
            maxResults=max_results).execute()
    else:
        return False
    # 循环获取完所有的结果
    nextPageToken = res.get('nextPageToken')
    while ('nextPageToken' in res):
        nextPage = youtube.playlists().list(
            part='snippet',
            channelId=youtube_channel_id,
            # maxResults=int(max_results),
            pageToken=nextPageToken
        ).execute()

        res['items'] = res['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            res.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']

    youtube_playlist_list = []
    for result in res.get("items", []):
        # 查询看该视频所属的channel是否保存到了数据库中
        channel = YouTubeChannel.objects.filter(
            channel_id=result['snippet']["channelId"]).first()
        # 如果视频所属的channel保存在YouTubeChannel中，
        # 也就是只下载已经保存到YouTubeChannel中的channel的playlist
        if channel:
            playlist = {
                'playlist_id': result['id'],
                'title': result['snippet']["title"],
                'channel': channel,
                'description': result['snippet']["description"],
                'thumbnail': result['snippet']['thumbnails']['default']['url']
            }

            d = dateutil.parser.parse(result['snippet']['publishedAt'])
            youtube_playlist, created = \
                YouTubePlaylist.objects.update_or_create(
                    playlist_id=playlist['playlist_id'],
                    defaults={'title': playlist['title'],
                              'publishedAt': d,
                              'thumbnail': playlist['thumbnail'],
                              'channel': channel
                              }
                )

            youtube_playlist_list.append(playlist)
    return youtube_playlist_list


def get_youtube_playlist_video_info(youtube_playlist_id, max_results, user):
    """
    获取youtube_playlist_id的所有video的信息
    :param youtube_playlist_id:
    :param max_results:最大为50
    :param user:
    :return:
    https://developers.google.com/apis-explorer/#p/youtube/v3/youtube
    .playlistItems.list
    """
    # filter()返回的是一个list，就算只有一个结果
    playlist = YouTubePlaylist.objects.filter(
        playlist_id=youtube_playlist_id).first()
    #youtube = get_authenticated_service(user)
    youtube = get_authenticated_service_s2s()
    if youtube:
        res = youtube.playlistItems().list(
            part='snippet, contentDetails',
            playlistId=youtube_playlist_id,
            maxResults=max_results).execute()

        # 将该playlist包含的视频数量保存到YouTubePlaylist中
        if res:
            video_num = res['pageInfo']['totalResults']
            playlist.video_num = video_num
            playlist.save(update_fields=['video_num'])
    else:
        return False

    # 循环获取完所有的结果
    nextPageToken = res.get('nextPageToken')
    while ('nextPageToken' in res):
        nextPage = youtube.playlistItems().list(
            part='snippet, contentDetails',
            playlistId=youtube_playlist_id,
            maxResults=max_results,
            pageToken=nextPageToken
        ).execute()

        res['items'] = res['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            res.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']

    video_list = []
    for result in res.get("items", []):
        # 查询看该视频所属的channel是否保存到了数据库中
        channel = YouTubeChannel.objects.filter(
            channel_id=result['snippet']["channelId"]).first()
        # 如果视频所属的channel保存在YouTubeChannel中，并且is_download属性为true
        # 也就是只下载已经保存到YouTubeChannel中的channel的视频
        if channel and channel.is_download:
            video = {
                'video_id': result['contentDetails']["videoId"],
                'title': result['snippet']["title"],
                'publishedAt': result['snippet']["publishedAt"],
                'thumbnail': result['snippet']['thumbnails']['default']['url'],
                'channel': channel,
                'playlist': playlist
            }

            # publishedAt 为ISO 8601 (
            # YYYY-MM-DDThh:mm:ss.sZ)格式，类似2008-09-26T01:51:42.000Z
            d = dateutil.parser.parse(video['publishedAt'])

            # 将获取到的playlist的视频信息保存到数据库的Video model中
            youtube_video, created = Video.objects.update_or_create(
                video_id=video['video_id'],
                defaults={'title': video['title'],
                          'publishedAt': d,
                          'thumbnail': video['thumbnail'],
                          'channel': channel,
                          'playlist': video['playlist']
                          }
            )
            video_list.append(video)
    return video_list
