# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-11 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20160307_2207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='gender',
        ),
        migrations.AlterField(
            model_name='driver',
            name='mobile_prefix',
            field=models.IntegerField(default=45),
        ),
    ]