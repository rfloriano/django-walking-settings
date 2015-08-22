# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('walking_settings', '0002_auto_20150805_2337'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ShadowSettings',
        ),
    ]
