# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-06 21:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63, unique=True)),
                ('slug', models.SlugField(help_text='A label for URL config.', max_length=31, unique=True)),
                ('date_updated', models.DateField(verbose_name='date last seen in this place')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('slug', models.SlugField(help_text='A label for URL config.', max_length=31, unique=True)),
                ('description', models.TextField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('slug', models.SlugField(help_text='A label for URL config.', max_length=31, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='place',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.Room'),
        ),
        migrations.AddField(
            model_name='item',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.Place'),
        ),
    ]
