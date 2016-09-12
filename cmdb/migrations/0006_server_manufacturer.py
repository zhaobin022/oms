# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0005_server_productname'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='manufacturer',
            field=models.CharField(max_length=20, null=True, verbose_name='\u5382\u5546', blank=True),
        ),
    ]
