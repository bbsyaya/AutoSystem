# coding=utf-8
from __future__ import unicode_literals

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

