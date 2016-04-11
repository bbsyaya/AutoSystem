from django.conf.urls import patterns, include, url
from django.contrib import admin

from AutoSystem.settings import DEBUG, MEDIA_ROOT, STATIC_ROOT

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'AutoSystem.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'manage_rss/', include('manage_rss.urls')),

                       url(r'^tinymce/', include('tinymce.urls')),
                       url(r'^video/', include('video.urls', namespace="video"),
                           # url(r'^youtube/', include('django_youtube.urls')),
                           ),
                       url(r'^oauth2/', include('oauth2_authentication.urls',
                                                namespace="oauth2")),

                       )

# urlpatterns += patterns('',
#     url(r'^django-rq/', include('django_rq.urls')),
# )

# urlpatterns += patterns('',
#     (r'^admin/rq/', include('django_rq_dashboard.urls')),
# )

if DEBUG:
    urlpatterns += patterns('', url(r'^media/(?P<path>.*)$',
                                    'django.views.static.serve',
                                    {'document_root': MEDIA_ROOT}),
                            url(r'^static/(?P<path>.*)$',
                                'django.views.static.serve',
                                {'document_root': STATIC_ROOT}), )

    import debug_toolbar

    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
