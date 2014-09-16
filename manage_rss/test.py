# coding=utf-8
from __future__ import unicode_literals

__author__ = 'GoTop'

from urllib import unquote
url = 'https://www.google.com/url?rct=j&ampsa=t&ampurl=http://www.givemesport.com/503692-fernando-torres-lured-to-ac-milan-by-filippo-inzaghi&ampct=ga&ampcd=CAIyGjQxNGI1YzIyNjczODU5NjM6Y29tOmVuOlVT&ampusg=AFQjCNF7ArVnX1q5rxYIfBXNPgmazWGWMQ'
url = url.split('&ampct')
url = url[0].replace(
    "https://www.google.com/url?rct=j&ampsa=t&ampurl=",
    '')



print url
#print  unquote(url)

