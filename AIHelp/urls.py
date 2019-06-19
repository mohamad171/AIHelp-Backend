
from django.urls import path,include
from django.contrib import admin


urlpatterns = [

    path('', include('smarthome.urls')),
    path('',include('webSite.urls')),

    path('panel/admin/', admin.site.urls),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
]
