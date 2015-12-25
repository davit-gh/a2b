# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-25 10:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20151225_0950'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fromwhere', models.CharField(max_length=100, verbose_name='From')),
                ('towhere', models.CharField(max_length=100, verbose_name='To')),
                ('leavedate', models.DateField(blank=True)),
            ],
            options={
                'verbose_name': 'User Search',
                'verbose_name_plural': 'User Searches',
            },
        ),
    ]
