# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-12 11:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motric', '0019_auto_20170110_0713'),
    ]

    operations = [
        migrations.AddField(
            model_name='labdevice',
            name='lab_location',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='requesteddevice',
            name='lab_location',
            field=models.CharField(blank=True, default='PEK', max_length=3, null=True),
        ),
    ]
