# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0024_auto_20160524_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='ssh_port',
            field=models.SmallIntegerField(default=22),
        ),
    ]
