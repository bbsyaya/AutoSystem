# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='YouTube',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vid_id', models.CharField(max_length=50)),
                ('vid_url', models.CharField(max_length=50)),
                ('playlist_url', models.URLField(max_length=300)),
                ('user', models.URLField(max_length=300)),
                ('keywords', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='video',
            options={},
        ),
    ]
