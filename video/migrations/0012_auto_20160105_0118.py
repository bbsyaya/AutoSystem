# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0011_auto_20160105_0105'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='yt_channel',
            options={'verbose_name': 'YouTube channel', 'verbose_name_plural': 'YouTube channels'},
        ),
        migrations.AlterField(
            model_name='yt_channel',
            name='category',
            field=models.ForeignKey(blank=True, to='video.Category', null=True),
        ),
    ]
