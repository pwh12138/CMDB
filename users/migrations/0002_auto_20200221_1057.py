# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-02-21 10:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'default_permissions': [], 'permissions': (('add_user', '添加用户'), ('show_user', '查看用户'), ('update_user', '更新用户'), ('delete_user', '删除用户'))},
        ),
    ]
