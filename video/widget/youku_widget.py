# coding=utf-8
from __future__ import unicode_literals

from django import forms
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

__author__ = 'GoTop'

class ButtonWidget(forms.Widget):
    """
    在youku model的edit page增加一个button widget
    """
    template_name = 'youku_button_widget.html'

    def render(self, name, value, attrs=None):
        youku = self.form_instance

        if youku.youku_video_id != '':
            #如果youku_video_id不为空，说明已经上传到优酷，则显示已经上传到优酷网站的视频链接
            youku_url = 'http://v.youku.com/v_show/id_%s.html' % youku.youku_video_id
            context = {
                'url': youku_url,
                'text': 'Youku 视频链接'
            }

        else:
            #如果youku_video_id为空，说明尚未上传到优酷，则显示上传到优酷网站操作链接
            # 显示上传video到优酷网站的链接
            publish_youku_url = reverse('video:youku_upload', args=[youku.video_id])

            context = {
                'url': publish_youku_url,
                'text': '上传到 Youku'
            }
        return mark_safe(render_to_string(self.template_name, context))

class UploadToYoukuWidget(forms.Widget):
    """
    在youku model的edit page增加一个button widget
    """
    template_name = 'youku_button_widget.html'

    def render(self, name, value, attrs=None):
        youku = self.form_instance

        if youku.youku_video_id == '':
            #如果youku_video_id为空，说明尚未上传到优酷，则显示上传到优酷网站操作链接
            publish_youku_url = reverse('video:youku_upload', args=[youku.video_id])
            context = {
                'url': publish_youku_url,
                'text': '上传视频到Youku'
            }
            return mark_safe(render_to_string(self.template_name, context))
        else:
            return mark_safe('')

class UpdateYoukuVideoWidget(forms.Widget):
    """
    在youku model的edit page增加一个button widget
    """
    template_name = 'youku_button_widget.html'

    def render(self, name, value, attrs=None):
        youku = self.form_instance

        if youku.youku_video_id != '':
            #如果youku_video_id不为空，说明已经上传到优酷，则显示已经上传到优酷网站的视频链接
            update_youku_url = reverse('video:update_youku_online_info', args=[youku.youku_video_id])
            context = {
                'url': update_youku_url,
                'text': '更新Youku信息'
            }
            return mark_safe(render_to_string(self.template_name, context))
        else:
            return mark_safe('')


class YoukuVideoUrlWidget(forms.Widget):
    """
    在youku model的edit page增加一个button widget
    """
    template_name = 'youku_button_widget.html'

    def render(self, name, value, attrs=None):
        youku = self.form_instance

        if youku.youku_video_id != '':
            #如果youku_video_id不为空，说明已经上传到优酷，则显示已经上传到优酷网站的视频链接
            youku_url = 'http://v.youku.com/v_show/id_%s.html' % youku.youku_video_id
            context = {
                'url': youku_url,
                'text': 'Youku 视频链接'
            }
            return mark_safe(render_to_string(self.template_name, context))

        else:
            return mark_safe('')