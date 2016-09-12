# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0011_auto_20160519_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='cmdbeventlog',
            name='event_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
