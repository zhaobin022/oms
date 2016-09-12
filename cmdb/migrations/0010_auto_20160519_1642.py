# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0009_auto_20160519_1336'),
    ]

    operations = [
        migrations.CreateModel(
            name='CmdbEventLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_type', models.SmallIntegerField(blank=True, null=True, choices=[(0, b'Create Server Info'), (1, b'Update Server Info')])),
                ('content', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': '\u670d\u52a1\u5668\u914d\u7f6e\u66f4\u65b0\u4e8b\u4ef6',
                'verbose_name_plural': '\u670d\u52a1\u5668\u914d\u7f6e\u66f4\u65b0\u4e8b\u4ef6',
            },
        ),
        migrations.RemoveField(
            model_name='app',
            name='task',
        ),
        migrations.RemoveField(
            model_name='server',
            name='application',
        ),
        migrations.DeleteModel(
            name='App',
        ),
        migrations.DeleteModel(
            name='TaskLog',
        ),
        migrations.AddField(
            model_name='cmdbeventlog',
            name='server',
            field=models.ForeignKey(blank=True, to='cmdb.Server', null=True),
        ),
    ]
