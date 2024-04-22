from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class item(models.Model):
    itemname = models.CharField(max_length=550,blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='', blank=True, null=True)
    category = models.CharField(max_length=225)
    unit = models.CharField(max_length=255,blank=True, null=True)
    saleprice = models.PositiveIntegerField(default=0)
    purchaseprice = models.PositiveIntegerField(default=0)
    stockbalance = models.IntegerField(default=0)
    subitem = models.CharField(max_length=255,blank=True, null=True)
    unpackqty = models.PositiveIntegerField(default=1)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.itemname

class invoicedetail(models.Model):
    member = models.CharField(max_length=100, blank=True, null=True)
    customer = models.CharField(max_length=100, blank=True, null=True)
    total_amount = models.PositiveIntegerField(default=0)
    created_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer

class invoiceitem(models.Model):
    invoice = models.ForeignKey(invoicedetail, on_delete=models.CASCADE)
    item = models.ForeignKey(item, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)
    subtotal = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.item