# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_rss', '0010_auto_20140914_1804'),
    ]

    operations = [
        migrations.CreateModel(
            name='PubInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_id', models.CharField(max_length=6)),
                ('pub_date', models.DateTimeField(null=True, blank=True)),
                ('site', models.ForeignKey(to='manage_rss.Site')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='article',
            name='pub_status',
        ),
        migrations.RemoveField(
            model_name='article',
            name='publish_date',
        ),
        migrations.AddField(
            model_name='article',
            name='pub_info',
            field=models.ForeignKey(to='manage_rss.PubInfo', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='review_status',
            field=models.CharField(default=b'decline', max_length=1, choices=[(b'publishable', b'Publishable'), (b'decline', b'Decline')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='context',
            field=tinymce.models.HTMLField(),
        ),
    ]
