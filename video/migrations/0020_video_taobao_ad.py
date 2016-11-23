# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth2_authentication', '0001_initial'),
        ('video', '0019_auto_20160828_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='taobao_ad',
            field=models.ForeignKey(to='oauth2_authentication.CredentialsModel', null=True),
        ),
    ]
