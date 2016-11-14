# coding=utf-8
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from ad.views import import_taobaoke_excel_view

__author__ = 'GoTop'

from django.conf.urls import patterns, url


urlpatterns = [
    # http://127.0.0.1:8000/ad/import_taobaoke_excel
    url(r'^import_taobaoke_excel$', import_taobaoke_excel_view,
        name='import_taobaoke_excel'),
]
