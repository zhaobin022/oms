# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0012_cmdbeventlog_event_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='cpu_core_count',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='CPU\u5185\u6838\u6570', blank=True),
        ),
    ]
