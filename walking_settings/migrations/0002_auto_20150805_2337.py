# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('walking_settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 5, 23, 37, 55, 578124), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shadowsettings',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 5, 23, 37, 57, 161695), auto_now=True),
            preserve_default=False,
        ),
    ]
