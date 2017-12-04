# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse

from django.shortcuts import render

# Create your views here.
from pandas import json
from models import danceRecord as dr
from models import storeImg as si
from PIL import Image
import os
import SqueezeHeader as sh


def toDance(request):

    print 'Enter toDance ....'

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

    print 'Enter getDance ...'

    if(request.method == 'GET'):
        return render(request, "getDance.html")

    if(request.method == 'POST'):
        data = request.POST

        day = data.get('time')
        place = data.get('place')

        print day, place

        pair = {}

        res = dr.objects.filter(day=day, place=place).values()

        print res

        if(res):
            for item in res:
                pair[item['name']] = item['hour']
            return HttpResponse(json.dumps(pair))
        else:
            return HttpResponse(json.dumps({'none'}))

def successPage(request):

    return render(request, "success.html")

def recordPage(request):

    return render(request, "team.html")

def showTeam(request):

    return render(request, "team.html")

def uploadImg(request):

    print 'uploadImg'
    return render(request, "success.html")

def uploadImg(request):

    if request.method == 'POST':
        new_img = si(
            img=request.FILES.get('img'),
            name = request.FILES.get('img').name
        )
        new_img.save()

    # img = Image.open('/home/siudong/myGit/forDance/media/img/timg.jpeg')
    # img.show()
    return render(request, 'uploading.html')

def showImg(request):
    imgs = si.objects.all()
    content = {
        'imgs':imgs,
    }
    for i in imgs:
        # i.img.url = '/home/siudong/myGit/forDance' + i.img.url
        print i.img.url

    return render(request, 'showing.html', content)



def routerClass(request):

    if request.method == 'GET':
        return render(request, 'router.html', {'index': 0})

    if request.method == 'POST':

        img = request.FILES.get('img')

        dir = '/home/siudong/myGit/forDance/media/img'

        img_name = str(img).decode(encoding='UTF-8')

        # 检查服务器端是否已经有同名图片
        res = si.objects.filter(name=img.name)
        image_path = os.path.join(dir, img.name)

        if res:
            print 'already exists(delete it)'
            res.delete()
            os.remove(image_path)
        else:
            print 'new img'

        # 保存新图片并插入数据库
        new_img = si(
            img=img,
            name=img.name
        )
        new_img.save()

        # 使用squeezenet判断图片中的路由器的型号
        prob = sh.get_prob_of_target(image_path)

        print image_path

        index = prob.index(max(prob)) + 1

        print index

        return render(request, 'router.html', {'index': index})