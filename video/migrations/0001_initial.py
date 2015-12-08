# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaiduYun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uri', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('url', models.URLField(max_length=300)),
                ('title_cn', models.CharField(max_length=50)),
                ('subtile_en', models.CharField(max_length=50)),
                ('subtile_cn', models.CharField(max_length=50)),
                ('remark', models.CharField(max_length=300, null=True, blank=True)),
                ('baiduy_yun', models.ForeignKey(blank=True, to='video.BaiduYun', null=True)),
            ],
            options={
                'verbose_name_plural': 'videos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Youku',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video_id', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='video',
            name='youku',
            field=models.ForeignKey(blank=True, to='video.Youku', null=True),
            preserve_default=True,
        ),
    ]
