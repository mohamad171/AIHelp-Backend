from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [

    path('panel/index',views.Index,name='main'),
    path('signin',views.login,name='login'),
    path('signup',views.register,name='register'),
    path('submitcode',views.submitCode,name='submitcode'),
    path('panel/applications',views.addApplicaion,name='addapplication'),
    path('panel/applications/get',views.getapplications,name='getapps'),
    path('panel/applications/delete',views.deleteapplication,name='deleteapplications'),
    path('panel/helpers',views.helpers,name='helpers'),
    path('panel/helpers/delete',views.deletehelpers,name='deletehelpers'),
    path('panel/addhtoapp',views.addhtoapp,name='addhtoapp'),
    path('panel/chats',views.chat,name='getChats'),
    path('panel/addMessageHelp',views.MessageHelper,name='MessageHelper'),
    path('api/setDeviceId',views.setDeviceId,name='setDeviceId'),
    path('api/createChat',views.CreateChat,name='CreateChat'),
    path('',views.main,name='landing'),
    path('jeebCGJAXJGGOTLU37J7ZJOUCY6JRTAODI.html',views.jeeb,name='jeeb'),



]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)