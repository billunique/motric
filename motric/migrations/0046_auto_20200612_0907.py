# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-06-12 09:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motric', '0045_quotadevice'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotadevice',
            name='shared_device',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='quotadevice',
            name='model_type',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='quotadevice',
            name='pe_poc',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
