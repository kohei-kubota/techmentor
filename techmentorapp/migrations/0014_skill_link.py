# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-10 18:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techmentorapp', '0013_auto_20161231_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='link',
            field=models.CharField(default='link', max_length=50),
            preserve_default=False,
        ),
    ]
