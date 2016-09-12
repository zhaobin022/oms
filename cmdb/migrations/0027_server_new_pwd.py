# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0026_auto_20160525_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='new_pwd',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
    ]
