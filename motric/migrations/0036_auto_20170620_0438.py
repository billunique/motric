# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-20 04:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motric', '0035_auto_20170608_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='requesteddevice',
            name='used_for',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='malfunction',
            name='type',
            field=models.CharField(choices=[('101', 'Cannot power on'), ('102', 'Screen cannot go light'), ('103', 'Screen touch broken'), ('104', 'Scramble screen'), ('105', 'Wifi hardware broken'), ('106', 'SDcard broken'), ('107', 'Battery broken'), ('108', 'Screen fragmentation'), ('201', 'Disconnected(usb)'), ('202', 'Offline(usb)'), ('203', 'Unauthorized(usb)'), ('204', 'Lose internet connection'), ('205', 'Stuck on fastboot screen'), ('206', 'Stuck on splash screen'), ('207', 'Stuck on white screen'), ('208', 'Reboot loop'), ('209', 'Not able to be reset'), ('1001', 'Others')], max_length=4),
        ),
    ]
