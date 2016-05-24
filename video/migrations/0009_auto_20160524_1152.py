# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0008_auto_20160405_2159'),
    ]

    operations = [
        migrations.RenameModel("YT_channel", "YouTubeChannel")
    ]
