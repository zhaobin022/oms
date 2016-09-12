# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0004_auto_20160518_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='productname',
            field=models.CharField(max_length=30, null=True, verbose_name='\u4ea7\u54c1\u578b\u53f7', blank=True),
        ),
    ]
