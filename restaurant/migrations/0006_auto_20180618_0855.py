# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-18 07:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0005_restaurantlocation_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantlocation',
            name='files',
            field=models.FileField(blank=True, max_length=120, null=True, upload_to='profile_pic'),
        ),
    ]
