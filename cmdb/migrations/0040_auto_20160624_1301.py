# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0039_auto_20160617_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servergroup',
            name='servers',
            field=models.ManyToManyField(to='cmdb.Server', blank=True),
        ),
    ]
