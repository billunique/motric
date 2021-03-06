# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-30 07:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('motric', '0015_auto_20160922_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='motric.RequestedDevice'),
        ),
        migrations.AlterField(
            model_name='event',
            name='device',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='motric.LabDevice'),
        ),
        migrations.AlterField(
            model_name='labdevice',
            name='owner',
            field=models.CharField(blank=True, default='', max_length=100),
            preserve_default=False,
        ),
    ]
