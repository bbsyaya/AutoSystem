# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0028_auto_20160123_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='youkuplaylist',
            name='youku',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='video.Youku'),
            preserve_default=True,
        ),
    ]
