# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=300)),
                ('title', models.CharField(max_length=300)),
                ('context', models.CharField(max_length=300)),
                ('status', models.CharField(max_length=1, choices=[(b'u', b'unread'), (b'r', b'read'), (b'd', b'decline')])),
                ('grab_data', models.DateTimeField(auto_now_add=True)),
                ('publish_date', models.DateTimeField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rss',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=300)),
                ('remark', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='article',
            name='rss',
            field=models.ForeignKey(to='manage_rss.Rss'),
            preserve_default=True,
        ),
    ]
