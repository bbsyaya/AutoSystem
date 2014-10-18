# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_rss', '0018_auto_20141004_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='editable_status',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rss',
            name='group',
            field=models.ForeignKey(related_name='related_rss', blank=True, to='manage_rss.Group', null=True),
        ),
    ]
