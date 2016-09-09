# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-08 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motric', '0009_labdevice_replaced_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='labdevice',
            name='respond_to',
            field=models.ManyToManyField(to='motric.RequestedDevice'),
        ),
        migrations.RemoveField(
            model_name='labdevice',
            name='model',
        ),
        migrations.AddField(
            model_name='labdevice',
            name='model',
            field=models.CharField(default='MotricAsset', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='labdevice',
            name='replaced_by',
            field=models.ManyToManyField(to='motric.LabDevice'),
        ),
    ]
