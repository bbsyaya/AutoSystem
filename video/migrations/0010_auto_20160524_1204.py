# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0009_auto_20160524_1152'),
    ]

    operations = [
        migrations.CreateModel(
            name='YouTubePlaylist',
            fields=[
                ('channel_id', models.URLField(max_length=100, serialize=False, primary_key=True)),
            ],
        ),
        migrations.AlterField(
            model_name='video',
            name='allow_upload_youku',
            field=models.BooleanField(default='True', help_text='\u662f\u5426\u53ef\u4ee5\u4e0a\u4f20\u5230\u4f18\u9177\uff0c\u9ed8\u8ba4\u4e3aTrue', verbose_name='\u662f\u5426\u4e0a\u4f20'),
        ),
        migrations.AlterField(
            model_name='video',
            name='remark',
            field=models.CharField(max_length=300, verbose_name='\u4f18\u9177\u6807\u9898', blank=True),
        ),
    ]
