# coding=utf-8
from __future__ import unicode_literals, absolute_import

from AutoSystem.settings import YOUKU_CLIENT_ID

from youku import YoukuPlaylists

from oauth2_authentication.function.youku import youku_get_authenticate
from video.function.playlist_config import \
    get_youku_playlist_from_playlist_config
from video.function.youku import youku_upload
from video.function.youtube_download import download_single_youtube_video_main
from video.function.youtube_playlist import get_youtube_playlist_video_info
from video.function.youtube_subtitle import download_subtitle
from video.models import PlaylistConfig, Video

CLIENT_ID = YOUKU_CLIENT_ID
__author__ = 'GoTop'


def set_youku_playlist_online(youku_video_id, playlist_id):
    """
    根据youku的youkuplaylist属性，在优酷网上将youku对象添加到该playlist中

    一个视频可以加入多个playlist，所以在youku中设置playlist后，如果不执行del_videos_from_playlist
    操作，视频仍然属于该playlist
    :param youku_id:
    :return:
    """

    service = YoukuPlaylists(CLIENT_ID)
    youku_access_token = youku_get_authenticate()
    # http://doc.open.youku.com/?docid=377
    # 视频ID用逗号来分割,每个专辑最多200个视频，限制单次操作视频的最大个数，默认20
    # video_ids=850,860,870,880
    # 返回的是专辑ID
    playlist_id = service.add_videos_to_playlist(
        access_token=youku_access_token,
        playlist_id=playlist_id,
        video_ids=youku_video_id)

    if playlist_id:
        return playlist_id
    else:
        return False


def set_youku_playlist_online_from_config_playlist(video_id):
    """
    根据上传到优酷的视频的video_id的YouTube上的playlist，设置视频在优酷上的playlist
    数据库中youtube_playlist与youku_playlist是多对多关系
    :param youku_video_id:
    :return:
    """
    playlist_id_list = get_youku_playlist_from_playlist_config(video_id)

    if playlist_id_list:
        video = Video.get(video_id=video_id)
        setted_playlist_id_list = []
        for playlist_id in playlist_id_list:
            setted_playlist_id = set_youku_playlist_online(
                video.youku_video_id, playlist_id)
            setted_playlist_id_list.append(setted_playlist_id)
        return setted_playlist_id_list
    else:
        return False


def delete_video_from_playlist(youku_video_id, playlist_id):
    """
    在playlist_id的优酷playlist中删除youku_video_id视频
    :param youku_video_id:
    :param playlist_id:
    :return:
    """
    service = YoukuPlaylists(CLIENT_ID)
    youku_access_token = youku_get_authenticate()

    try:
        id = service.del_videos_from_playlist(access_token=youku_access_token,
                                              playlist_id=playlist_id,
                                              video_ids=youku_video_id)
    except:
        # 如果playlist_id中没有youku_video_id，会提示异常，忽略即可
        pass
        return False

    if id:
        return id
    else:
        return False


def get_youku_playlist():
    """
    获取认证用户的playlist
    :return:
    """
    service = YoukuPlaylists(CLIENT_ID)
    youku_access_token = youku_get_authenticate()
    # http://doc.open.youku.com/?docid=377
    # 视频ID用逗号来分割,每个专辑最多200个视频，限制单次操作视频的最大个数，默认20
    # video_ids=850,860,870,880
    playlist_json = service.find_playlists_by_me(
        access_token=youku_access_token,
        orderby='published', page=1, count=20)


def download_playlist_video(num, user):
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
                    .playlist_id, max_results=int(num), user=user)
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
                        download_single_youtube_video_main(video_id,
                                                           max_retey=5,
                                                           file_extend='mp4')
                        download_subtitle(video_id)

                        download_num = download_num + 1
                        if download_num <= num:
                            break
            else:
                video_list = []
                text = '获取youtube playlist的视频信息失败'
    return result_list

# def upload_playlist_video(num, user):
#     upload_num = 0
#     # 如果该视频已下载，但是未上传到优酷，则上传
#     if video.is_upload == False:
#         # video对象还没有创建对应的youku对象怎么办？
#         youku_upload(video.youku.id)
#         # 在优酷上设置视频的playlist
#         set_youku_playlist_online_from_config_playlist(video_id)
#         upload_num = upload_num + 1
#         if upload_num <= num:
#             break
#     result_list.append({'download_num': download_num,
#                         'upload_num': upload_num,
#                         'text': text})