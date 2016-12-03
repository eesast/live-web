# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-22 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('live', '0003_auto_20161122_1655'),
    ]

    operations = [
        migrations.CreateModel(
            name='Givenid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authid', models.CharField(max_length=4)),
            ],
        ),
        migrations.RemoveField(
            model_name='guest',
            name='msg_count',
        ),
        migrations.RemoveField(
            model_name='msg',
            name='sender',
        ),
        migrations.AddField(
            model_name='msg',
            name='img',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='msg',
            name='name',
            field=models.CharField(default='Anonymous', max_length=20),
        ),
    ]
