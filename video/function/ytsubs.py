#!/usr/bin/env python
# coding=utf-8

# Copyright (C) 2014 Alistair Buxton <a.j.buxton@gmail.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom
# the Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import urllib2
import json
import itertools
import os
import sys
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

"""
将用户订阅的频道最新上传的视频信息生成rss文件
能减少使用api的quota数
https://github.com/ali1234/ytsubs

暂时先不使用
2015-12-27

"""
# 参考 https://github.com/ali1234/ytsubs
# http://stackoverflow.com/questions/19640796/retrieving-all-the-new-subscription-videos-in-youtube-v3-api/
baseurl = 'https://www.googleapis.com/youtube/v3'
# my_key = os.environ.get('YOUTUBE_SERVER_API_KEY')
my_key = 'AIzaSyAp4Dr7YgwofjNbosQ5VZFXm8G5A1QNIPQ'

# check for missing inputs
if not my_key:
    print "YOUTUBE_SERVER_API_KEY variable missing."
    sys.exit(-1)

if not len(sys.argv) >= 2:
    print "username and (optionally) destination file must be specified as first and second arguments."
    sys.exit(-1)


def get_channel_for_user(user):
    """
    通过用户名获取用户的channel
    :param user:
    :return:
    """
    url = baseurl + '/channels?part=id&forUsername=' + user + '&key=' + my_key
    response = urllib2.urlopen(url)
    data = json.load(response)
    return data['items'][0]['id']


def get_playlists(channel):
    """
    通过用户的channel获取用户订阅的50个channel的uploaded videos的playlist的playlist Id

    :param channel:
    :return:
    """
    playlists = []
    # we have to get the full snippet here, because there is no other way to get the channelId
    # of the channels you're subscribed to. 'id' returns a subscription id, which can only be
    # used to subsequently get the full snippet, so we may as well just get the whole lot up front.
    url = baseurl + '/subscriptions?part=snippet&channelId=' + channel + '&maxResults=50&order=unread&key=' + my_key

    next_page = ''
    while len(playlists) < 50:
        # we are limited to 50 results. if the user subscribed to more than 50 channels
        # we have to make multiple requests here.
        # 获取用户订阅的50个channel的channel Id,
        # 如果用户订阅的channel多余50个，以下代码会多次运行，直至获取完所有的channel Id为止（imgotop订阅了474个channel）
        response = urllib2.urlopen(url + next_page)
        data = json.load(response)
        subs = []
        for i in data['items']:
            if i['kind'] == 'youtube#subscription':
                subs.append(i['snippet']['resourceId']['channelId'])

        # actually getting the channel uploads requires knowing the upload playlist ID, which means
        # another request. luckily we can bulk these 50 at a time.
        #一次性获取50个订阅的channel的“上传视频”这个playlist的playlist Id
        purl = baseurl + '/channels?part=contentDetails&id=' + '%2C'.join(subs) + '&maxResults=50&key=' + my_key
        response = urllib2.urlopen(purl)
        data2 = json.load(response)
        for i in data2['items']:
            try:
                playlists.append(i['contentDetails']['relatedPlaylists']['uploads'])
            except KeyError:
                pass

        try:  # loop until there are no more pages
            next_page = '&pageToken=' + data['nextPageToken']
        except KeyError:
            break

    return playlists


def get_playlist_items(playlist):
    videos = []

    if playlist:
        # get the last 5 videos uploaded to the playlist
        # 在url里设置了maxResults=5
        url = baseurl + '/playlistItems?part=contentDetails&playlistId=' + playlist + '&maxResults=5&key=' + my_key
        response = urllib2.urlopen(url)
        data = json.load(response)
        for i in data['items']:
            if i['kind'] == 'youtube#playlistItem':
                videos.append(i['contentDetails']['videoId'])

    return videos


def get_real_videos(video_ids):
    videos = []
    purl = baseurl + '/videos?part=snippet&id=' + '%2C'.join(video_ids) + '&maxResults=50&key=' + my_key
    response = urllib2.urlopen(purl)
    data = json.load(response)

    return data['items']


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def do_it():
    username = sys.argv[1]

    # get all upload playlists of subbed channels
    playlists = get_playlists(get_channel_for_user(username))

    # get the last 5 items from every playlist
    allitems = []
    for p in playlists:
        allitems.extend(get_playlist_items(p))

    # the playlist items don't contain the correct published date, so now
    # we have to fetch every video in batches of 50.
    allvids = []
    for chunk in chunks(allitems, 50):
        allvids.extend(get_real_videos(chunk))

    # sort them by date
    sortedvids = sorted(allvids, key=lambda k: k['snippet']['publishedAt'], reverse=True)


    # build the rss
    rss = Element('rss')
    rss.attrib['version'] = '2.0'
    channel = SubElement(rss, 'channel')
    title = SubElement(channel, 'title')
    title.text = 'Youtube subscriptions for ' + username
    link = SubElement(channel, 'link')
    link.text = 'http://www.youtube.com/'

    # add the most recent 20
    for v in sortedvids[:20]:
        item = SubElement(channel, 'item')
        title = SubElement(item, 'title')
        title.text = v['snippet']['title']
        link = SubElement(item, 'link')
        link.text = 'http://youtube.com/watch?v=' + v['id']
        author = SubElement(item, 'author')
        author.text = v['snippet']['channelTitle']
        guid = SubElement(item, 'guid')
        guid.attrib['isPermaLink'] = 'true'
        guid.text = 'http://youtube.com/watch?v=' + v['id']
        pubDate = SubElement(item, 'pubDate')
        pubDate.text = v['snippet']['publishedAt']
        description = SubElement(item, 'description')
        description.text = v['snippet']['description']

    if len(sys.argv) >= 3:
        filename = sys.argv[2]
        f = open(filename, 'w')
    else:
        f = sys.stdout

    f.write('<?xml version="1.0" encoding="UTF-8" ?>')
    f.write(tostring(rss).encode('utf-8'))
    f.close()


if __name__ == '__main__':
    for i in range(3):
        try:
            do_it()
        except urllib2.HTTPError, error:
            if error.code == 500:
                continue
            raise error
        break