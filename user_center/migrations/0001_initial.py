# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(unique=True, max_length=255, verbose_name=b'username')),
                ('is_active', models.BooleanField(default=True)),
                ('admin_tag', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('alias', models.CharField(max_length=64, null=True, blank=True)),
                ('position', models.SmallIntegerField(blank=True, null=True, choices=[(0, b'\xe4\xba\xa7\xe5\x93\x81\xe7\xbb\x8f\xe7\x90\x86'), (1, b'\xe6\xb5\x8b\xe8\xaf\x95\xe7\xbb\x8f\xe7\x90\x86'), (2, b'\xe5\xbc\x80\xe5\x8f\x91\xe7\xbb\x8f\xe7\x90\x86'), (3, b'\xe8\xbf\x90\xe7\xbb\xb4\xe4\xba\xba\xe5\x91\x98'), (4, b'\xe8\xbf\x90\xe7\xbb\xb4\xe7\xbb\x8f\xe7\x90\x86'), (5, b'\xe6\x8a\x80\xe6\x9c\xaf\xe7\xbb\x8f\xe7\x90\x86'), (6, b'\xe8\xb6\x85\xe7\xba\xa7\xe7\xae\xa1\xe7\x90\x86\xe5\x91\x98')])),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('phone', models.CharField(max_length=64, null=True, blank=True)),
                ('description', models.CharField(max_length=20, null=True, verbose_name='\u4eba\u5458\u63cf\u8ff0', blank=True)),
                ('header_image', models.CharField(max_length=64, null=True, blank=True)),
                ('friends', models.ManyToManyField(related_name='friends_set', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'verbose_name': '\u7cfb\u7edf\u7528\u6237',
                'verbose_name_plural': '\u7cfb\u7edf\u7528\u6237',
            },
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(unique=True, max_length=30)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': '\u7cfb\u7edf\u7ec4',
                'verbose_name_plural': '\u7cfb\u7edf\u7ec4',
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='group',
            field=models.ForeignKey(blank=True, to='user_center.UserGroup', null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='team_member',
            field=models.ManyToManyField(related_name='team_leader_set', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]
