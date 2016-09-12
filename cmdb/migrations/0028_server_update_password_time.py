# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0027_server_new_pwd'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='update_password_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
