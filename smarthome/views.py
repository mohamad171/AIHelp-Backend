from django.shortcuts import render
from django.http import HttpResponse
from smarthome.models import *
import json
from django.views.decorators.csrf import csrf_exempt

def getHome(request , homeid):
    home = Home.objects.get(id=homeid)
    jdata = {
        "HomeName": home.HomeName,
        "HomeAddress": home.HomeAddress
    }
    return HttpResponse(json.dumps({"home":jdata}))

def getBulb(request,bulbId):
    bulb = Bulb.objects.get(id=bulbId)

    jdata = {
        "BulbName":bulb.BulbName,
        "BulbHome":bulb.Home.HomeName,
        "BulbStatus":bulb.BublStatus
    }
    return HttpResponse(json.dumps({"bulb":jdata}))

def getBublbStatus(request,bulbId):
        bulb = Bulb.objects.get(id=bulbId)
        return HttpResponse(bulb.BublStatus)

@csrf_exempt
def setBulb(request,bulbId):
    if request.method == "POST":
        bulb = Bulb.objects.get(id=bulbId)
        if request.POST.get("status") == "1":
            bulb.BublStatus = True
        else:
            bulb.BublStatus = False
        bulb.save()

        return HttpResponse(json.dumps({"status":"ok"}))
    else:
        return HttpResponse("Faild")


