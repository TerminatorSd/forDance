# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from pandas import json
from models import danceRecord as dr


def toDance(request):

    if(request.method == "GET"):
        return render(request, "index.html")

    if(request.method == 'POST'):
        data = request.POST

        name = data.get('name')
        time = data.get('time').split('T')
        place = data.get('place')

        day = time[0]
        hour = time[1]

        print name, day, hour, place

        res = dr.objects.filter(name=name, day=day)
        if(res):
            res.update(name=name, day=day, hour=hour, place=place)
            print "Already exists, replace it."
        else:
            dr.objects.create(name=name, day=day, hour=hour, place=place)
            print "Inser into the database."

        return HttpResponse(json.dumps({'ok'}))


def getDance(request):

    if(request.method == 'GET'):
        return render(request, "getDance.html")

    if(request.method == 'POST'):
        data = request.POST

        day = data.get('time')
        place = data.get('place')

        print day, place

        pair = {}

        res = dr.objects.filter(day=day, place=place).values()

        if(res):
            for item in res:
                pair[item['name']] = item['hour']
            return HttpResponse(json.dumps(pair))
        else:
            return HttpResponse(json.dumps({'none'}))

def successPage(request):

    return render(request, "success.html")

def recordPage(request):

    return render(request, "record.html")