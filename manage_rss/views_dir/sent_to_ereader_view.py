# coding=utf-8
from __future__ import unicode_literals
from django.shortcuts import render_to_response
from kindle_reader.kindlereader import KindleReader
from manage_rss.function.rss import gen_group_rss_url

__author__ = 'GoTop'


def sent_rss_to_ereader_view(request):
    group_rss_urls = gen_group_rss_url()
    kr = KindleReader(group_rss_urls)
    # kr.main()

    return render_to_response('result.html',
                              {'text': '将group rss 发送到 ereader！'})
