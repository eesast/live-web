# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-22 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('live', '0002_auto_20161117_2043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='city',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='country',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='fake_id',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='province',
        ),
        migrations.AddField(
            model_name='guest',
            name='authid',
            field=models.CharField(default=0, max_length=4),
        ),
        migrations.AlterField(
            model_name='guest',
            name='msg_count',
            field=models.IntegerField(default=0),
        ),
    ]
