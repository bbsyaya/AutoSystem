from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'oauth2callback', views.oauth2callback_view, name='return'),

    url(r'get_playlists', views.get_playlists_view, name='return'),

    url(r'search/(?P<q>\w+)/(?P<max_results>\d+)$', views.search_view, name='search'),
)