# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0034_auto_20160614_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='actionoperation',
            name='script_path',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
