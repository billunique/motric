# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-10 07:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motric', '0018_requesteddevice_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requesteddevice',
            name='comment',
            field=models.CharField(max_length=256),
        ),
    ]
