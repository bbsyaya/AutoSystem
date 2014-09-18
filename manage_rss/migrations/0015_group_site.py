# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_rss', '0014_auto_20140918_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='site',
            field=models.ForeignKey(default=1, to='manage_rss.Site'),
            preserve_default=False,
        ),
    ]
