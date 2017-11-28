# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class danceRecord(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    day = models.CharField(max_length=20)
    hour = models.CharField(max_length=20)
    place = models.CharField(max_length=30)

class storeImg(models.Model):
    img = models.ImageField(upload_to='img')
    name = models.CharField(max_length=20)