# coding=utf-8
from __future__ import unicode_literals


__author__ = 'GoTop'

import os
import httplib2
import argparse

from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


# CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__),'client_secret_505556718060-0q2mpuukae9m5uqj88fofllecigllf2l.apps.googleusercontent.com.json')
# CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__),'client_secret_405726684174-8fbsgk9dgk1cj2tl08p5rac8pndnqno9.apps.googleusercontent.com.json')

CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__),
                                   'client_secret_505556718060-20u5pd4rd7sgeigqmdc5o5rvt1ifjtfk.apps.googleusercontent.com.json')

YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                               scope=YOUTUBE_READ_WRITE_SCOPE,
                               redirect_uri='http://localhost:8000/oauth2callback')

storage = Storage('storage.json')
# storage.locked_delete()
credentials = storage.get()

# parser = argparse.ArgumentParser(parents=[argparser])
# flags = parser.parse_args()
#
# flags = argparse.ArgumentParser(parents=[argparser]).parse_args()

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[argparser])
flags = parser.parse_args()

if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, flags)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                http=credentials.authorize(httplib2.Http()))

channels_response = youtube.channels().list(
    mine=True,
    part="contentDetails"
).execute()

for channel in channels_response["items"]:
    # From the API response, extract the playlist ID that identifies the list
    # of videos uploaded to the authenticated user's channel.
    uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]

print "Videos in list %s" % uploads_list_id

# Retrieve the list of videos uploaded to the authenticated user's channel.
playlistitems_list_request = youtube.playlistItems().list(
    playlistId=uploads_list_id,
    part="snippet",
    maxResults=50
)

while playlistitems_list_request:
    playlistitems_list_response = playlistitems_list_request.execute()

    # Print information about each video.
    for playlist_item in playlistitems_list_response["items"]:
        title = playlist_item["snippet"]["title"]
        video_id = playlist_item["snippet"]["resourceId"]["videoId"]
        print "%s (%s)" % (title, video_id)

    playlistitems_list_request = youtube.playlistItems().list_next(
        playlistitems_list_request, playlistitems_list_response)

print