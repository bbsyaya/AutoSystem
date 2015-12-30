# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0006_video_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='file',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
