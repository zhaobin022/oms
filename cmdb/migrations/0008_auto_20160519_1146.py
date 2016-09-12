# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0007_auto_20160519_0949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='cpu_groups',
        ),
        migrations.AddField(
            model_name='server',
            name='physical_cpu_count',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='CPU\u7269\u7406\u4e2a\u6570', blank=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='cpu_nums',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='CPU\u6570', blank=True),
        ),
    ]
