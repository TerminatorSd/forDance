# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-03 07:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='danceRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('day', models.CharField(max_length=20)),
                ('hour', models.CharField(max_length=20)),
                ('place', models.CharField(max_length=30)),
            ],
        ),
    ]
