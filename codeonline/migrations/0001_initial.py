# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlineRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('request_time', models.DateTimeField(auto_now_add=True, verbose_name='\u7533\u8bf7\u65f6\u95f4')),
                ('function_type', models.IntegerField(blank=True, null=True, verbose_name='\u529f\u80fd\u7c7b\u578b', choices=[(1, b'app'), (2, b'bug'), (3, b'both')])),
                ('test_result_tag', models.BooleanField(default=False, verbose_name='\u6d4b\u8bd5\u7ed3\u679c')),
                ('version_tag', models.CharField(max_length=30, verbose_name='\u7248\u672c\u6807\u8bc6', blank=True)),
                ('online_function', models.TextField(verbose_name='\u4e0a\u7ebf\u529f\u80fd')),
                ('online_files', models.TextField(verbose_name='\u4e0a\u7ebf\u6587\u4ef6')),
                ('online_operation', models.IntegerField(blank=True, null=True, verbose_name='\u53d1\u7248\u662f\u5426\u9700\u8981\u5982\u4e0b\u64cd\u4f5c', choices=[(1, '\u91cd\u542f\u7f13\u5b58'), (2, '\u5b9a\u65f6\u4efb\u52a1')])),
                ('suggest_update_time', models.DateTimeField(null=True, verbose_name='\u5efa\u8bae\u4e0a\u7ebf\u65f6\u95f4', blank=True)),
                ('update_code_time', models.DateTimeField(null=True, verbose_name='\u4ee3\u7801\u4e0a\u7ebf\u65f6\u95f4', blank=True)),
                ('online_request_status', models.IntegerField(blank=True, null=True, verbose_name='\u6d41\u7a0b\u72b6\u6001', choices=[(1, '\u4ea7\u54c1\u7ecf\u7406\u5df2\u63d0\u4ea4\u7533\u8bf7'), (2, '\u4e0a\u7ebf\u524d\u5f00\u53d1\u7ec4\u957f\u5df2\u786e\u8ba4'), (3, '\u4e0a\u7ebf\u524d\u6d4b\u8bd5\u7ecf\u7406\u5df2\u786e\u8ba4'), (4, '\u4e0a\u7ebf\u524d\u6280\u672f\u7ecf\u7406\u5df2\u786e\u8ba4'), (5, '\u8fd0\u7ef4\u4e0a\u7ebf\u5df2\u786e\u8ba4'), (6, '\u8fd0\u7ef4\u7ecf\u7406\u4e0a\u7ebf\u5df2\u786e\u8ba4'), (7, '\u6d4b\u8bd5\u7ecf\u7406\u4e0a\u7ebf\u540e\u5df2\u786e\u8ba4'), (8, '\u4ea7\u54c1\u7ecf\u7406\u4e0a\u7ebf\u540e\u5df2\u786e\u8ba4(\u5b8c\u7ed3)')])),
                ('app', models.ManyToManyField(to='cmdb.App', verbose_name='\u4e0a\u7ebf\u9879\u76ee')),
            ],
            options={
                'verbose_name': '\u4e0a\u7ebf\u6d41\u7a0b\u8868',
                'verbose_name_plural': '\u4e0a\u7ebf\u6d41\u7a0b\u8868',
            },
        ),
    ]
