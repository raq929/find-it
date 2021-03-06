# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-27 16:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0007_auto_20161205_0310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(help_text='A label for URL config.', max_length=31, unique=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='slug',
            field=models.SlugField(help_text='A label for URL config.', max_length=31, unique=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='slug',
            field=models.SlugField(help_text='A label for URL config.', max_length=31, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='place',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='item',
            name='house',
        ),
        migrations.RemoveField(
            model_name='place',
            name='house',
        ),
    ]
