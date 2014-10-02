# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_rss', '0016_auto_20140928_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rss',
            name='url',
            field=models.URLField(max_length=300),
        ),
    ]
