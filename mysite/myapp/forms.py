from django import forms
from django.forms import inlineformset_factory
from .models import *
class invoicedetailform(forms.ModelForm):
    class Meta:
        model = invoicedetail
        fields = '__all__'
        # widgets = {

class invoiceitemform(forms.ModelForm):
    class Meta:
        model = invoiceitem
        fields = '__all__'
        widgets = {
            'item':forms.Select(attrs={'class':' itemselect', 'width':'300px'}),
        }


VariantFormSet = inlineformset_factory(
    invoicedetail, invoiceitem, form=invoiceitemform,
    extra=1, can_delete=True,
    can_delete_extra=True
)