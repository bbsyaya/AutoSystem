# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0032_auto_20160209_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='subtitle_cn',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='subtitle_en',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='subtitle_merge',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='title_cn',
            field=models.CharField(max_length=150, blank=True),
            preserve_default=True,
        ),
    ]
