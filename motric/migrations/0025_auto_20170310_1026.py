# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 10:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motric', '0024_requesteddevice_bug_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='labdevice',
            name='po_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='labdevice',
            name='price_cny',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='labdevice',
            name='price_usd',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True),
        ),
    ]
