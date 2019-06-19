from django.contrib import admin
from smarthome.models import *


class HomeAdmin(admin.ModelAdmin):

    list_display = ('id','HomeName', 'HomeAddress')

class BulbAdmin(admin.ModelAdmin):

    list_display = ('id','BulbName', 'Home','BublStatus','LastModify')

admin.site.register(Home,HomeAdmin)
admin.site.register(Bulb,BulbAdmin)

