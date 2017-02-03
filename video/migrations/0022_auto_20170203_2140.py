# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0021_auto_20161124_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubeplaylist',
            name='is_download',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='video',
            name='taobao_ad',
            field=models.ForeignKey(blank=True, to='ad.TaoBao', null=True),
        ),
    ]
