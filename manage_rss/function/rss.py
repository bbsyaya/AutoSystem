# coding=utf-8
from __future__ import unicode_literals
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import request
from kindle_reader.kindlereader import KindleReader
from ..models import Group


__author__ = 'GoTop'

from urllib import quote


def gen_fivefilters_rss(rss_url):
    '''
    使用http://fivefilters.org/content-only/ 将非全文rss转化为全文rss
    该函数返回fivefilters.org转化后的rss链接
    :param rss_url:
    :return:
    '''
    url_prefix = 'http://ftr.fivefilters.org/makefulltextfeed.php?url='
    return   url_prefix + quote(rss_url)

def gen_group_rss_url():
    '''
    生成所有group的rss链接
    :return:
    '''
    group_rss_urls = []
    for group in Group.objects.all():
        domain=Site.objects.get_current()
        abslute_url = domain.name + reverse("group_rss_url",args=[group.slug])
        group_rss_urls.append(abslute_url)
    return group_rss_urls

