# coding=utf-8
from __future__ import unicode_literals

from django import forms
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from video.models import Youku, Video

__author__ = 'GoTop'


class ButtonWidget(forms.Widget):
    """
    在youku model的edit page增加一个button widget
    """

    # def __init__(self, obj, attrs=None):
    #     self.object = obj
    #     super(ButtonWidget, self).__init__(attrs)

    #todo 研究如何将使用该form的model传入widget
    # def __init__(self, *args, **kwargs):
    #     self.obj = kwargs.pop('obj', None)
    #     super(ButtonWidget, self).__init__(*args, **kwargs)

    template_name = 'youku_button_widget.html'

    def render(self, name, value, attrs=None):
        # 显示上传video到优酷网站的链接
        publish_youku_url = reverse('video:youku_upload', args=[self.obj.video_id])

        context = {
            'url': '/'
        }
        return mark_safe(render_to_string(self.template_name, context))


class YoukuForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(YoukuForm, self).__init__(*args, **kwargs)
        youku = kwargs.pop('instance', None)
        self.fields['button'].widget.obj = youku

    class Meta:
        model = Youku

        # 覆盖默认的widget
        # https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#overriding-the-default-fields
        widgets = {
            'title': forms.TextInput(attrs={'size': 100}),
            'tags': forms.TextInput(attrs={'size': 100}),
        }
        fields = '__all__'  # Register your models here.

    # todo 研究获取将使用该form的model，构造admin url传给widget
    button = forms.CharField(widget=ButtonWidget(attrs={'instance': 1}))


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video

        # 覆盖默认的widget
        # https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#overriding-the-default-fields
        widgets = {
            'title': forms.TextInput(attrs={'size': 100}),
            'title_cn': forms.TextInput(attrs={'size': 100}),
            'subtitle_en': forms.TextInput(attrs={'size': 100}),
            'subtitle_cn': forms.TextInput(attrs={'size': 100}),
            'subtitle_merge': forms.TextInput(attrs={'size': 100}),
            'file': forms.TextInput(attrs={'size': 100}),
            'subtitle_video_file': forms.TextInput(attrs={'size': 100}),
        }
        fields = '__all__'  # Register your models here.
