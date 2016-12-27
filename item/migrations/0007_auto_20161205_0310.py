# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-05 03:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0006_room_house'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='house',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='item.House'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='place',
            name='house',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='item.House'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(help_text='A label for URL config.', max_length=31),
        ),
        migrations.AlterField(
            model_name='place',
            name='slug',
            field=models.SlugField(help_text='A label for URL config.', max_length=31),
        ),
        migrations.AlterField(
            model_name='room',
            name='slug',
            field=models.SlugField(help_text='A label for URL config.', max_length=31),
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('slug', 'house')]),
        ),
        migrations.AlterUniqueTogether(
            name='place',
            unique_together=set([('slug', 'house')]),
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together=set([('slug', 'house')]),
        ),
    ]
