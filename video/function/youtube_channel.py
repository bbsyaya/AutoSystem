# coding=utf-8
from __future__ import unicode_literals, absolute_import

from oauth2_authentication.function.google_oauth2_server_to_server import \
    get_authenticated_service_s2s
from oauth2_authentication.views import get_authenticated_service
from video.models import YouTubeChannel

__author__ = 'GoTop'


def get_youtube_channel_info(channel_id, user):
    """
    根据channel_id,获取channel的信息，并保存到数据库中

    https://developers.google.com/youtube/v3/docs/channels/list#try-it

    GET https://www.googleapis.com/youtube/v3/channels?part=contentDetails
    %2Csnippet&id=UCEQpJTOXGkvS1UQsdCm6lLA&key={YOUR_API_KEY}

    :param channel_id:
    :param user:
    :return:
    """
    #youtube = get_authenticated_service(user)
    youtube = get_authenticated_service_s2s()

    if youtube:
        res = youtube.channels().list(
            part='snippet',
            id=channel_id).execute()
    else:
        return False

    # channel_info_list = []
    # for result in res.get("items", []):
    #     channel_info_list.append(result['snippet'])

    channel_info = res.get("items", [])[0]['snippet']

    channel, created = YouTubeChannel.objects.update_or_create(
        channel_id=channel_id,
        defaults={'title': channel_info['title'],
                  'description': channel_info['description'],
                  'thumbnail': channel_info['thumbnails']['default']['url']
                  }
    )

    return channel_info
