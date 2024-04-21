from django.contrib import admin
from .models import *
# Register your models here.
class itemnameadmin(admin.ModelAdmin):
    list_display = ('id', 'itemname', 'saleprice')
admin.site.register(item,itemnameadmin)