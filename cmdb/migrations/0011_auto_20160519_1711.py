# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0010_auto_20160519_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmdbeventlog',
            name='content',
            field=models.TextField(),
        ),
    ]
