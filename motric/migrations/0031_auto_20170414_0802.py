# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-14 08:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motric', '0030_auto_20170414_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labdevice',
            name='os',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
