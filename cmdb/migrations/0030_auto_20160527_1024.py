# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0029_auto_20160525_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventlog',
            name='log_type',
            field=models.SmallIntegerField(choices=[(0, b'execute command'), (1, b'update code'), (2, b'install software'), (3, b'update password')]),
        ),
    ]
