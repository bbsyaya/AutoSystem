# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_rss', '0006_auto_20140831_2134'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('url', models.URLField(max_length=300)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='article',
            name='status',
        ),
        migrations.AddField(
            model_name='article',
            name='pub_status',
            field=models.CharField(default=b'u', max_length=1, choices=[(b'unpublish', b'unPublish'), (b'published', b'Published'), (b'publishable', b'Publishable'), (b'decline', b'Decline')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='read_status',
            field=models.CharField(default=b'u', max_length=1, choices=[(b'u', b'unRead'), (b'r', b'Read')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rss',
            name='type',
            field=models.CharField(default=b'normal_rss', max_length=50, choices=[(b'google_alert', b'Google Alert'), (b'normal_rss', b'Normal Rss')]),
        ),
    ]
