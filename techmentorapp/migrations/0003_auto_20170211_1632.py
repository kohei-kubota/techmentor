# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-11 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techmentorapp', '0002_auto_20170211_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(max_length=255, unique=True),
        ),
    ]
