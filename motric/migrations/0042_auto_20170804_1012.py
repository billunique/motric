# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-04 10:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motric', '0041_auto_20170803_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchhistory',
            name='q_type',
            field=models.IntegerField(default=0),
        ),
    ]
