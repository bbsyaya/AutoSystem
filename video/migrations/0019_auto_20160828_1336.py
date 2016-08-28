# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0018_auto_20160827_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtubechannel',
            name='channel_id',
            field=models.CharField(max_length=100, serialize=False, primary_key=True),
        ),
    ]
