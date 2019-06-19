from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from . import DBModel
import json
import hashlib
import random
import redis
import time
from redisearch import *

redis = redis.Redis(host='localhost', port=6379, db=0)

def jeeb(request):
    return render(request,"jeebCGJAXJGGOTLU37J7ZJOUCY6JRTAODI.html")
def main(request):
    return  render(request,"index.html")

def Index(request):
    if "islogin" in request.session and "userid" in request.session:
        if request.session["islogin"] and request.session["userid"] != None:
            userdata = DBModel.WebsiteUsers.objects(id=request.session["userid"]).get()
            userjson = {"Name":userdata.Fname + " "+userdata.Lname , "Credit":userdata.Credit}
            return render(request,"main.html",context={"userdata":userjson})
        else:
            return redirect("login")
    else:
        return redirect("login")



@csrf_exempt
def setDeviceId(request):
    deviceid = request.POST.get("deviceid")
    DBModel.Users.objects(DeviceId=deviceid).update_one(set__DeviceId=deviceid,
                                                                set__LastLogin=str(int(time.time())), upsert=True)
    return HttpResponse("ok")

@csrf_exempt
def addhtoapp(request):
    if "islogin" in request.session and "userid" in request.session:
        if request.session["islogin"] and request.session["userid"] != None:
            if request.method == "POST":
                helperid = request.POST.get("helperid")
                userdata = DBModel.WebsiteUsers.objects(id=request.session["userid"]).get()
                apps = DBModel.Applications.objects(Owner=userdata).get()
                helper = DBModel.Helpers.objects(id=helperid).get()

                if helper not in apps.AllowUsers:
                    apps.update(add_to_set__AllowUsers=[helper])
                    return HttpResponse(json.dumps({"status":"ok"}))
                else:
                    return HttpResponse(json.dumps({"status": "exist"}))

        else:
            return redirect("login")
    else:
        return redirect("login")

@csrf_exempt
def MessageHelper(request):
    answer = request.POST.get("answer")
    question = request.POST.get("question")

    app = DBModel.Applications.objects(id=request.POST.get("AppId")).get()

    client = Client(app.PackageName)
    client.add_document(generateid(4), answer = answer, question = question)

    messagehelp = DBModel.MessageHelper()
    messagehelp.Answer = answer
    messagehelp.Question = question
    messagehelp.App = app
    messagehelp.save()
    return HttpResponse(json.dumps({"status":"ok"}))


@csrf_exempt
def CreateChat(request):
    if request.method == "POST":
        appid = request.POST.get("appId")
        deviceid = request.POST.get("deviceid")
        backupemail = request.POST.get("email")
        additional = request.POST.get("additional")
        packagename = request.POST.get("packageName")
        print(packagename)

        try:

            app = DBModel.Applications.objects(id=appid).get()

            if app.PackageName == packagename:

                user = DBModel.Users.objects(DeviceId=deviceid).get()
                trackid = generateid(6)

                if app.Credit - 500  >= 0:
                    DBModel.Applications.objects(id=appid).update_one(dec__Credit=500)
                    chats = DBModel.Chats()
                    chats.AdditionalFields = additional
                    chats.App = app
                    chats.BackUpEmail = backupemail
                    chats.TrackingId = trackid
                    chats.User = user
                    chats.save()
                    currentchat = DBModel.Chats.objects(TrackingId = trackid).get()
                    return HttpResponse(json.dumps({"status": "ok", "message": "چت با موفقیت ساخته شد", "ChatId": str(currentchat.id)}))
                else:
                    return HttpResponse(json.dumps({"status":"credit","message":"اعتبار اپلیکیشن به پایان رسیده"}))
            else:
                return HttpResponse(json.dumps({"status": "package", "message": "پکیج نیم ارسال شده و اپلیکیشن آیدی همخوانی ندارد"}))
        except:
            return HttpResponse(json.dumps({"status": "notexist", "message": "اپلیکیشن با آیدی وارد شده موجود نمیباشد"}))
    else:
        return HttpResponse("Must be post \n")


@csrf_exempt
def deleteapplication(request):
    if "islogin" in request.session and "userid" in request.session:
        if request.session["islogin"] and request.session["userid"] != None:
            if request.method == "POST":
                appid = request.POST.get("appid")
                app = DBModel.Applications.objects(id=appid).get()
                DBModel.WebsiteUsers.objects(id=request.session["userid"]).update_one(inc__Credit=app.Credit)

                DBModel.Applications.objects(id=appid).delete()
                return HttpResponse(json.dumps({"status":"ok"}))
        else:
            return redirect("login")
    else:
        return redirect("login")

@csrf_exempt
def getChats(request):
    if "islogin" in request.session and "userid" in request.session:
        if request.session["islogin"] and request.session["userid"] != None:
            if request.method == "POST":
                print("OK")
            else:
                userdata = DBModel.WebsiteUsers.objects(id=request.session["userid"]).get()
                userjson = {"Name": userdata.Fname + " " + userdata.Lname, "Credit": userdata.Credit}
                return render(request, "chats.html",
                              context={"userdata": userjson})
        else:
            return redirect("login")
    else:
        return redirect("login")


@csrf_exempt
def addApplicaion(request):
    if "islogin" in request.session and "userid" in request.session:
        if request.session["islogin"] and request.session["userid"] != None:
            if request.method == "POST":
                packagename = request.POST.get("packagename")
                appname = request.POST.get("appname")
                try:
                    apps = DBModel.Applications.objects(PackageName = packagename).get()
                    return HttpResponse(json.dumps({"status":"packagename"}))
                except DBModel.DoesNotExist:

                    userdata = DBModel.WebsiteUsers.objects(id=request.session["userid"]).get()
                    if userdata.Credit >= 5000:
                        helper = DBModel.Helpers.objects(Email = request.session["email"]).get()
                        appdata = DBModel.Applications()
                        appdata.AppName = appname
                        appdata.PackageName = packagename
                        appdata.Owner = userdata
                        appdata.Credit = 5000

                        appdata.AllowUsers = [helper]
                        appdata.save()



                        client = Client(packagename)
                        client.create_index((TextField('question', weight=5.0), TextField('answer')))


                        DBModel.WebsiteUsers.objects(id=request.session["userid"]).update_one(dec__Credit=5000)
                        return HttpResponse(json.dumps({"status": "ok"}))
                    else:
                        return HttpResponse(json.dumps({"status": "credit"}))
            else:
                userdata = DBModel.WebsiteUsers.objects(id=request.session["userid"]).get()
                userjson = {"Name":userdata.Fname + " "+userdata.Lname , "Credit":userdata.Credit}
                helperarr = []
                helpers = DBModel.Helpers.objects()
                print(request.session["userid"])
                for helper in helpers:
                            jdata = {
                                "id": str(helper.id),
                                "Name": helper.Name,
                                "Email": helper.Email,
                                "isActive": helper.isActive
                            }
                            helperarr.append(jdata)
                apparr = []
                apps = DBModel.Applications.objects(Owner=userdata)
                for app in apps:
                    jdata = {
                        "AppId": app.id,
                        "Appname": app.AppName,
                        "PackageName": app.PackageName,
                        "HelpersCount": len(app.AllowUsers),
                        "AppCredit": app.Credit
                    }
                    apparr.append(jdata)

                return render(request,"addapplication.html",context={"userdata":userjson,"apps":apparr,"helpers":helperarr})
        else:
            return redirect("login")
    else:
        return redirect("login")



@csrf_exempt
def deletehelpers(request):
    if "islogin" in request.session and "userid" in request.session:
        if request.session["islogin"] and request.session["userid"] != None:
            if request.method == "POST":
                helperid = request.POST.get("helperid")
                DBModel.Helpers.objects(id=helperid).delete()
                return HttpResponse(json.dumps({"status":"ok"}))
        else:
            return redirect("login")
    else:
        return redirect("login")

@csrf_exempt
def getapplications(request):
    if "islogin" in request.session and "userid" in request.session:
        if request.session["islogin"] and request.session["userid"] != None:
            appid = request.POST.get("appid")
            inhelperarr = []
            apps = DBModel.Applications.objects(id = appid).get()

            for helper in apps.AllowUsers:
                    try:
                        jdata = {
                            "id": str(helper.id),
                            "Name": helper.Name,
                            "Email": helper.Email,
                            "isActive": helper.isActive
                        }
                        inhelperarr.append(jdata)
                    except AttributeError:
                        print("Delete")


            return HttpResponse(json.dumps({"status":"ok","inhelp":inhelperarr}))
        else:
            return redirect("login")
    else:
        return redirect("login")

@csrf_exempt
def helpers(request):
    if "islogin" in request.session and "userid" in request.session:
        if request.session["islogin"] and request.session["userid"] != None:
            if request.method == "DELETE":
                print(request.Get.get("Id"))
                return HttpResponse(json.dumps({"status":"ok"}))
            elif request.method == "POST":
                email = request.POST.get("email")
                password = request.POST.get("password")
                name = request.POST.get("helpername")
                try:
                    helper = DBModel.Helpers.objects(Email = email).get()
                    return HttpResponse(json.dumps({"status":"email"}))
                except DBModel.DoesNotExist:
                    helper = DBModel.Helpers()
                    helper.Password = hashlib.md5(password.encode("utf-8")).hexdigest()
                    helper.Name = name
                    helper.Email = email
                    helper.isActive = True
                    helper.save()
                    return HttpResponse(json.dumps({"status":"ok"}))

            else:
                userdata = DBModel.WebsiteUsers.objects(id=request.session["userid"]).get()
                userjson = {"Name":userdata.Fname + " "+userdata.Lname , "Credit":userdata.Credit}
                helperarr = []
                helpers = DBModel.Helpers.objects()
                for helper in helpers:
                    jdata = {
                        "id": str(helper.id),
                        "Name": helper.Name,
                        "Email": helper.Email,
                        "isActive": helper.isActive
                    }
                    helperarr.append(jdata)
                return render(request,"helpers.html",context={"userdata":userjson,"helpers":helperarr})
        else:
            return redirect("login")
    else:
        return redirect("login")
@csrf_exempt
def register(request):
    fname = request.POST.get("fname")
    lname = request.POST.get("lname")
    email = request.POST.get("email")
    password = request.POST.get("password")
    try:
        webusers = DBModel.WebsiteUsers.objects(Email = email).get()
        return HttpResponse(json.dumps({"status": "email"}))

    except DBModel.DoesNotExist:
        webusers = DBModel.WebsiteUsers()
        webusers.Fname = fname
        webusers.Lname = lname
        webusers.Email = email
        webusers.Password = hashlib.md5(password.encode('utf8')).hexdigest()
        webusers.Credit = 10000
        webusers.isActive = False
        webusers.save()
        EmailActivation(email,fname)
        request.session["email"] = email

        helper = DBModel.Helpers()
        helper.Name = fname +" "+ lname
        helper.Email = email
        helper.Password = hashlib.md5(password.encode('utf8')).hexdigest()
        helper.isActive = True
        helper.save()

        return HttpResponse(json.dumps({"status":"ok"}))

@csrf_exempt
def login(request):


    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:

            webuserdata = DBModel.WebsiteUsers.objects(Email = email).get()
            if hashlib.md5(password.encode("utf-8")).hexdigest() == webuserdata.Password:
                print(email)
                helper = DBModel.Helpers.objects(Email = email).get()
                request.session["email"] = email
                request.session["islogin"] = True
                request.session["userid"] = str(webuserdata.id)
                request.session["helperid"] = str(helper.id)

                return HttpResponse(json.dumps({"status":"ok"}))
            else:
                return HttpResponse(json.dumps({"status": "password"}))
        except DBModel.DoesNotExist:
            return HttpResponse(json.dumps({"status":"notexist"}))
    else:
        return render(request,"login.html")

@csrf_exempt
def chat(request):
    if "islogin" in request.session and "userid" in request.session:
        if request.session["islogin"] and request.session["userid"] != None:
            userdata = DBModel.WebsiteUsers.objects(id=request.session["userid"]).get()
            userjson = {"Name": userdata.Fname + " " + userdata.Lname, "Credit": userdata.Credit}
            helper = DBModel.Helpers.objects(id = request.session["helperid"]).get()

            chats = DBModel.Chats.objects()

            chatarr = []
            for l in chats:
                lastmessage = DBModel.Messages.objects(ChatId = l).order_by("-id").first()
                jdata = {
                    "id": str(l.id),
                    "TrackingId":l.TrackingId,
                    "AdditionalFields":l.AdditionalFields,
                    "lastMessage":lastmessage
                }
                chatarr.append(jdata)


            return render(request, "chat.html", context={"userdata": userjson,"chats":chatarr})
        else:
            return redirect("login")
    else:
        return redirect("login")





@csrf_exempt
def submitCode(request):
    if request.method == "POST":
        code = request.POST.get("code")
        email = request.session["email"] if "email" in request.session else None

        if redis.exists(code):
            if redis.get(code).decode("utf-8")  == email:
                customer = DBModel.WebsiteUsers.objects(Email=email).get()
                customer.isActive = True
                customer.save()
                helper = DBModel.Helpers()
                helper.Name = customer.Fname +" "+customer.Lname
                helper.Email = customer.Email
                helper.Password = customer.Password
                helper.isActive = True
                helper.save()

                request.session["islogin"]=True

                redis.delete(code)
                return HttpResponse(json.dumps({"status":"ok"}))
            else:
                return HttpResponse(json.dumps({"status":"code"}))
        else:
            return HttpResponse(json.dumps({"status":"code"}))

def generateid(lenofstring):
    s = "0123456789"
    passlen = lenofstring
    p =  "".join(random.sample(s,passlen ))
    return p

def EmailActivation(emailaddress,value):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "کد تایید هویت"
    msg['From'] = "mohamadmohamadi249@gmail.com"
    msg['To'] = emailaddress
    html = open("templates/validateemail.html","r").read()
    code = generateid(6)
    html = html.replace("{Code}",code).replace("{Name}",value)
    redis.set(code,emailaddress)
    redis.expire(code,120)

    emailpart = MIMEText(html, 'html')
    msg.attach(emailpart)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login("mohamadmohamadi249@gmail.com", "09382138446m")

    server.sendmail("mohamadmohamadi249@gmail.com", emailaddress, msg.as_string())
    server.quit()