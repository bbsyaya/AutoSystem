from django.conf.urls import patterns, include, url

from django.contrib import admin
from AutoSystem import settings

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'AutoSystem.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'manage_rss/', include('manage_rss.urls')),

                       url(r'^tinymce/', include('tinymce.urls')),

                       url(r'^youtube/', include('django_youtube.urls')),
                       url(r'^oauth2/', include('oauth2_authentication.urls', namespace="oauth2")),


)

if settings.DEBUG:
    urlpatterns += patterns('', url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                                    {'document_root': settings.MEDIA_ROOT}),
                            url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': settings.STATIC_ROOT}), )

