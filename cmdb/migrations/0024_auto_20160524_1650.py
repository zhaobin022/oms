# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0023_eventlog'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventlog',
            options={'verbose_name': '\u4e8b\u4ef6\u65e5\u5fd7', 'verbose_name_plural': '\u4e8b\u4ef6\u65e5\u5fd7'},
        ),
        migrations.AlterField(
            model_name='eventlog',
            name='log_type',
            field=models.SmallIntegerField(choices=[(0, b'execute command'), (1, b'update code'), (2, b'install software')]),
        ),
    ]
