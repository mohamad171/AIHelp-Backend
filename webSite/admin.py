from django.contrib import admin

from webSite.models import *

class CustomerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post,CustomerAdmin)
admin.site.register(Category,CustomerAdmin)
admin.site.register(Comment,CustomerAdmin)