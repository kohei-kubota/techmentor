# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-31 16:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techmentorapp', '0012_auto_20161228_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='available',
            name='time',
            field=models.CharField(default='10:00', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='available',
            name='date',
            field=models.CharField(max_length=100),
        ),
    ]