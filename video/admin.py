# coding=utf-8
from __future__ import unicode_literals
from adminbrowse import AutoBrowseModelAdmin, link_to_url, link_to_changelist, link_to_change

from django.contrib import admin
from .models import Video

# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_cn','url')

admin.site.register(Video, VideoAdmin)