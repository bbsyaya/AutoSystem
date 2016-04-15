# coding=utf-8
from __future__ import unicode_literals
from django import forms
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from video.models import Youku, Video
from video.widget.youku_widget import ButtonWidget, UploadToYoukuWidget, \
    YoukuVideoUrlWidget, UpdateYoukuVideoWidget

__author__ = 'GoTop'


class YoukuForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(YoukuForm, self).__init__(*args, **kwargs)

        # http://stackoverflow.com/questions/1226590/django-how-can-i-access-the-form-field-from-inside-a-custom-widget/2135739#2135739
        # From inside the Form class you can access the Model instance through self.instance. Remember the instance
        # will be rather blank when Add/Creating a new object.
        # 将form model传给 buttom widget
        self.fields['upload_to_youku'].widget.form_instance = self.instance
        self.fields['youku_video_url'].widget.form_instance = self.instance
        self.fields['update_youku_video'].widget.form_instance = self.instance

    class Meta:
        model = Youku

        # 覆盖默认的widget
        # https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#overriding-the-default-fields
        widgets = {
            'title': forms.TextInput(attrs={'size': 180}),
            'tags': forms.TextInput(attrs={'size': 180}),
        }
        fields = '__all__'  # Register your models here.

    # todo 研究获取将使用该form的model，构造admin url传给widget
    upload_to_youku = forms.CharField(widget=UploadToYoukuWidget(),
                                      required=False)
    youku_video_url = forms.CharField(widget=YoukuVideoUrlWidget(),
                                      required=False)
    update_youku_video = forms.CharField(widget=UpdateYoukuVideoWidget(),
                                         required=False)


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video

        # 覆盖默认的widget
        # https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#overriding-the-default-fields
        # widgets = {
        #     'title': forms.TextInput(attrs={'size': 180}),
        #     'subtitle_en': forms.TextInput(attrs={'size': 180}),
        #     'subtitle_cn': forms.TextInput(attrs={'size': 180}),
        #     'subtitle_merge': forms.TextInput(attrs={'size': 180}),
        #     'file': forms.TextInput(attrs={'size': 180}),
        #     'subtitle_video_file': forms.TextInput(attrs={'size': 180}),
        # }
        fields = '__all__'  # Register your models here.


class VideoChangeListForm(forms.ModelForm):
    # https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#overriding-the-default-fields

    class Meta:
        model = Video
        youku_title = forms.CharField()
        fields = youku_title


    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            initial = kwargs.get('initial', {})
            initial['youku_title'] = instance.youku.title
            kwargs['initial'] = initial
        super(VideoChangeListForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        # use whatever parsing you like here
        youku_title = self.cleaned_data['youku_title']
        self.youku.save(title = youku_title)
        super(VideoChangeListForm, self).save(*args, **kwargs)
