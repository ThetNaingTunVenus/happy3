from django.contrib import admin
from .models import *
# Register your models here.
class itemnameadmin(admin.ModelAdmin):
    list_display = ('id', 'itemname', 'saleprice')
admin.site.register(item,itemnameadmin)

class invoicedetailadmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'created_date')
admin.site.register(invoicedetail, invoicedetailadmin)


class invoiceitemadmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'qty', 'price', 'subtotal')
admin.site.register(invoiceitem, invoiceitemadmin)