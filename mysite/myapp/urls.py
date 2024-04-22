from django.urls import path
from .views import *
from . import views
app_name = 'myapp'
urlpatterns = [
    path('test/',testview.as_view(), name='testview'),
    path('invoicelist/', invoicelist.as_view(), name='invoicelist'),
    path('create/', InvoiceCreate.as_view(), name='create_invoice'),
    path('update/<int:pk>/', InvoiceUpdate.as_view(), name='update_invoice'),

    path('delete-variant/<int:pk>/', delete_variant, name='delete_variant'),
    ]