# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('codeonline', '0003_onlinerequest_assign_developer_leader'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlinerequest',
            name='assign_developer_leader',
            field=models.ForeignKey(verbose_name='\u5206\u914d\u5f00\u53d1\u7ec4', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
