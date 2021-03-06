# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-06-07 13:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_capacity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostCapacityApiCheckRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=64, verbose_name='ip')),
                ('mounted', models.CharField(max_length=64, verbose_name='mounted')),
                ('used_percent', models.CharField(max_length=64, verbose_name='used_percent')),
                ('check_time', models.DateTimeField(auto_now=True, verbose_name='check time')),
            ],
            options={
                'verbose_name': 'API磁盘容量查询记录',
                'verbose_name_plural': 'API磁盘容量查询记录',
            },
        ),
    ]
