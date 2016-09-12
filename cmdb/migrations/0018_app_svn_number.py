# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0017_app'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='svn_number',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
