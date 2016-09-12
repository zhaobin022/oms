# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0020_auto_20160523_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='application',
            field=models.ForeignKey(verbose_name='\u5e94\u7528', blank=True, to='cmdb.App', null=True),
        ),
    ]
