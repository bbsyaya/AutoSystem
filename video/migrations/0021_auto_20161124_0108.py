# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0020_video_taobao_ad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='taobao_ad',
            field=models.ForeignKey(to='ad.TaoBao', null=True),
        ),
    ]
