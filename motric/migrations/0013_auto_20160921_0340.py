# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-21 03:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motric', '0012_auto_20160909_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='requesteddevice',
            name='resolved_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='requesteddevice',
            name='po_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]