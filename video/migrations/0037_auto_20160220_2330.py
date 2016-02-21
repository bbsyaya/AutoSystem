# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0036_auto_20160218_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yt_channel',
            name='category',
            field=models.ForeignKey(blank=True, to='video.Category', null=True),
        ),
    ]
