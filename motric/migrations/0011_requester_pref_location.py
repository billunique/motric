# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-09 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motric', '0010_auto_20160908_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='requester',
            name='pref_location',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]