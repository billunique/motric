# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-06 09:10
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('motric', '0007_auto_20160830_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event',
            field=jsonfield.fields.JSONField(),
        ),
    ]
