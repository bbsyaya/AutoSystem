# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0016_auto_20160107_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='youku',
            field=models.ForeignKey(blank=True, to='video.Youku', null=True),
        ),
    ]
