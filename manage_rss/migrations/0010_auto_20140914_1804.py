# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_rss', '0009_load_default_stier_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='grab_data',
            new_name='grab_date',
        ),
    ]
