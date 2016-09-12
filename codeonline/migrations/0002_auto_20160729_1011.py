# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('codeonline', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='onlinerequest',
            name='assign_developer_leader',
            field=models.ForeignKey(verbose_name='\u5206\u914d\u5f00\u53d1\u7ec4', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='onlinerequest',
            name='cto_confirm',
            field=models.ForeignKey(related_name='cto_confirm', verbose_name='CTO\u4e0a\u7ebf\u540e\u529f\u80fd\u786e\u8ba4', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='onlinerequest',
            name='developer',
            field=models.ManyToManyField(related_name='developer', verbose_name='\u5f00\u53d1\u4eba\u5458', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='onlinerequest',
            name='developer_fun_confirm_before_online',
            field=models.ForeignKey(related_name='developer_fun_confirm_before_online', verbose_name='\u5f00\u53d1\u4eba\u5458\u529f\u80fd\u786e\u8ba4', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='onlinerequest',
            name='maintenance_manager_comfirm',
            field=models.ManyToManyField(related_name='maintenance_manager_comfirm', verbose_name='\u8fd0\u7ef4\u7ecf\u7406\u786e\u8ba4', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='onlinerequest',
            name='maintenance_persion_comfirm',
            field=models.ManyToManyField(related_name='maintenance_persion_comfirm', verbose_name='\u8fd0\u7ef4\u4eba\u5458\u786e\u8ba4', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='onlinerequest',
            name='product_man_confirm_after_online',
            field=models.ManyToManyField(related_name='product_man_confirm_after_online', verbose_name='\u4ea7\u54c1\u4e0a\u7ebf\u540e\u529f\u80fd\u786e\u8ba4', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='onlinerequest',
            name='product_man_confirm_before_online',
            field=models.ManyToManyField(related_name='product_man_confirm_before_online', verbose_name='\u4ea7\u54c1\u7ecf\u7406\u4e0a\u7ebf\u524d\u786e\u8ba4', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='onlinerequest',
            name='require_side',
            field=models.ManyToManyField(related_name='require_side', verbose_name='\u9700\u6c42\u65b9', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='onlinerequest',
            name='technical_man_fun_confirm_online',
            field=models.ManyToManyField(related_name='technical_man_fun_confirm_online', verbose_name='\u6280\u672f\u7ecf\u7406\u529f\u80fd\u786e\u8ba4', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='onlinerequest',
            name='test_confirm_after_online',
            field=models.ManyToManyField(related_name='test_confirm_after_online', verbose_name='\u6d4b\u8bd5\u4eba\u5458\u4e0a\u7ebf\u540e\u529f\u80fd\u786e\u8ba4', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='onlinerequest',
            name='test_confirm_before_online',
            field=models.ManyToManyField(related_name='test_confirm_before_online', verbose_name='\u6d4b\u8bd5\u4eba\u5458\u4e0a\u7ebf\u524d\u529f\u80fd\u786e\u8ba4', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='onlinerequest',
            name='test_man_confirm_after_online',
            field=models.ManyToManyField(related_name='test_man_confirm_after_online', verbose_name='\u6d4b\u8bd5\u7ecf\u7406\u4e0a\u7ebf\u540e\u529f\u80fd\u786e\u8ba4', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='onlinerequest',
            name='white_box_test',
            field=models.ManyToManyField(related_name='white_box_test', verbose_name='\u767e\u76d2\u529f\u80fd\u786e\u8ba4', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
