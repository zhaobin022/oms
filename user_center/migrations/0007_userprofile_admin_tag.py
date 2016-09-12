# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_center', '0006_auto_20160524_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='admin_tag',
            field=models.BooleanField(default=False),
        ),
    ]
