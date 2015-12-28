# coding=utf-8
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from youku import YoukuVideos
CLIENT_ID = 'bdf4fcf59c05aff9'

def main():
    youku = YoukuVideos(CLIENT_ID)
    video = youku.find_video_by_id(VIDEO_ID)
