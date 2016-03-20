# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0003_auto_20160320_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='tags',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
