# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_rss', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rss',
            options={'verbose_name_plural': 'rss'},
        ),
        migrations.AlterField(
            model_name='article',
            name='context',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(default=b'u', max_length=1, choices=[(b'u', b'unread'), (b'r', b'read'), (b'd', b'decline')]),
        ),
    ]
