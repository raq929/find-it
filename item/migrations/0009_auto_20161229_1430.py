# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-29 14:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0008_auto_20161227_1614'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='room',
            unique_together=set([('slug', 'house')]),
        ),
    ]
