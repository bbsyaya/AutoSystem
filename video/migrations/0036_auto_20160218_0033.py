# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0035_auto_20160215_1617'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='title_cn',
        ),
        migrations.AlterField(
            model_name='video',
            name='file',
            field=models.FileField(default='', max_length=200, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='subtitle_cn',
            field=models.FileField(default='', max_length=200, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='subtitle_en',
            field=models.FileField(default='', max_length=200, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='subtitle_merge',
            field=models.FileField(default='', max_length=200, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='subtitle_video_file',
            field=models.FileField(default='', max_length=200, upload_to=b'', blank=True),
            preserve_default=True,
        ),

    ]
