from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [

    path('home/<homeid>/getHome',views.getHome,name='getHome'),
    path('bulb/<bulbId>/getBulb',views.getBulb,name='getBulb'),
    path('bulb/<bulbId>/getBulbStatus',views.getBublbStatus,name='getBublbStatus'),
    path('bulb/<bulbId>/setBulb',views.setBulb,name='setBulb'),

]