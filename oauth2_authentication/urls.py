from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    # http://127.0.0.1:8000/oauth2
    url(r'^$', views.index, name='index'),

    url(r'oauth2callback', views.oauth2callback_view, name='return'),

    # http://127.0.0.1:8000/oauth2/reauthenticate
    url(r'reauthenticate', views.reauthenticate_view),

)