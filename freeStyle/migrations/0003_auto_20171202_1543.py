# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 15:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freeStyle', '0002_storeimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storeimg',
            name='name',
            field=models.CharField(max_length=32),
        ),
    ]