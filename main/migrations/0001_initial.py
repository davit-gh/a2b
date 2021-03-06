# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-02 17:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_en', models.CharField(max_length=100)),
                ('name_hy', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'ab_city',
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='Contactus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='\u0531\u0576\u0578\u0582\u0576')),
                ('email', models.EmailField(max_length=254, verbose_name='\u0537\u056c\u2024 \u0583\u0578\u057d\u057f')),
                ('message', models.TextField(verbose_name='\u0546\u0561\u0574\u0561\u056f')),
                ('message_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'ab_contactus',
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_en', models.CharField(max_length=100)),
                ('name_hy', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'ab_country',
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=30)),
                ('licence_plate', models.CharField(default='19oo199', max_length=10)),
                ('gender', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'ab_driver',
                'verbose_name': 'Driver',
                'verbose_name_plural': 'Drivers',
            },
        ),
        migrations.CreateModel(
            name='DriverImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/images')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imgs', to='main.Driver')),
            ],
            options={
                'db_table': 'ab_driverimage',
                'verbose_name': 'Driver Image',
                'verbose_name_plural': 'Driver Images',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/images')),
                ('caption', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'db_table': 'ab_image',
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.CreateModel(
            name='Inboundmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('html_body', models.CharField(max_length=2000)),
                ('send_date', models.DateTimeField()),
                ('subject', models.CharField(max_length=100)),
                ('reply_to', models.CharField(max_length=100)),
                ('sender', models.CharField(max_length=100)),
                ('attachment', models.CharField(blank=True, max_length=400)),
            ],
            options={
                'db_table': 'ab_mail',
            },
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leavedate', models.DateField(blank=True)),
                ('starttime', models.TimeField(blank=True)),
                ('endtime', models.TimeField(blank=True, null=True)),
                ('price', models.IntegerField(blank=True)),
                ('passenger_number', models.IntegerField(default=2)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rides', to='main.Driver')),
                ('fromwhere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rides_from', to='main.City')),
                ('towhere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rides_to', to='main.City')),
            ],
            options={
                'db_table': 'ab_ride',
                'verbose_name': 'Ride',
                'verbose_name_plural': 'Rides',
            },
        ),
        migrations.CreateModel(
            name='UserSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fromwhere', models.CharField(max_length=100)),
                ('towhere', models.CharField(max_length=100)),
                ('leavedate', models.DateField(blank=True)),
            ],
            options={
                'db_table': 'ab_usersearch',
                'verbose_name': 'User Search',
                'verbose_name_plural': 'User Searches',
            },
        ),
        migrations.AddField(
            model_name='driver',
            name='featured_image',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.Image'),
        ),
        migrations.AddField(
            model_name='driver',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
