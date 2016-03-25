# coding=utf-8
from __future__ import unicode_literals

from django.conf.urls import patterns, url
# from . import views, youku_views
from oauth2_authentication import views, youku_views

urlpatterns = patterns(
    '',
    #############
    # Youtube认证
    #############
    # http://127.0.0.1:8000/oauth2
    url(r'^$', views.authenticate_view, name='index'),

    # http://127.0.0.1:8000/oauth2/authenticate
    url(r'^authenticate$', views.authenticate_view, name='authenticate'),

    url(r'^oauth2callback', views.oauth2callback_view, name='return'),

    # http://127.0.0.1:8000/oauth2/reauthorize
    url(r'^reauthorize$', views.reauthorize_view),


    ####################
    # 优酷认证
    ####################
    # http://127.0.0.1:8000/oauth2/youku_authenticate
    url(r'^youku_authenticate$', youku_views.youku_authenticate_view,name='youku_authenticate'),

    # http://127.0.0.1:8000/oauth2/youku_oauth2callback
    url(r'^youku_oauth2callback', youku_views.youku_oauth2callback_view),
)