# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_rss', '0004_auto_20140831_1327'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('keywords', models.CharField(max_length=100)),
                ('remark', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='rss',
            options={},
        ),
        migrations.AddField(
            model_name='rss',
            name='group',
            field=models.ForeignKey(default=0, to='manage_rss.Group'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rss',
            name='type',
            field=models.CharField(default=b'normal_rss', max_length=50, choices=[(b'google_alert', b'google alert'), (b'normal_rss', b'normal rss')]),
            preserve_default=True,
        ),
    ]
