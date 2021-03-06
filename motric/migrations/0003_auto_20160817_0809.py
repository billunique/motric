# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-17 08:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motric', '0002_auto_20160808_0336'),
    ]

    operations = [
        migrations.AddField(
            model_name='requesteddevice',
            name='lab_location',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='labdevice',
            name='status',
            field=models.CharField(choices=[('REQ', 'Requested'), ('APP', 'Approved'), ('REF', 'Refused'), ('ORD', 'Ordered'), ('REC', 'Received'), ('REG', 'Registered'), ('AVA', 'Public'), ('ASS', 'Assigned'), ('WIT', 'Withdrawn'), ('BRO', 'Broken'), ('REP', 'In repair'), ('RET', 'Retired (Recycled)')], max_length=3),
        ),
        migrations.AlterField(
            model_name='requesteddevice',
            name='po_number',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='requesteddevice',
            name='status',
            field=models.CharField(choices=[('REQ', 'Requested'), ('APP', 'Approved'), ('REF', 'Refused'), ('ORD', 'Ordered'), ('REC', 'Received'), ('REG', 'Registered'), ('AVA', 'Public'), ('ASS', 'Assigned'), ('WIT', 'Withdrawn'), ('BRO', 'Broken'), ('REP', 'In repair'), ('RET', 'Retired (Recycled)')], max_length=3),
        ),
    ]
