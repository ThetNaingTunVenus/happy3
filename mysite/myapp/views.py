from django.shortcuts import render
import datetime

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.db.models import Sum,Count,F
from django.http import HttpResponse
from django.views.generic import TemplateView, View, CreateView, DetailView,FormView,ListView,UpdateView
from django.contrib import messages
from django.views.generic.edit import DeleteView

from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator

from .forms import *
from .models import *
# Create your views here.

class testview(View):
    def get(self, request):
        return render(request, 'index.html')


class invoicelist(ListView):
    model = invoicedetail
    template_name = "invoice_list.html"
    context_object_name = "invoice"



class InvoiceInline():
    form_class = invoicedetailform
    model = invoicedetail
    template_name = "invoice_create_update.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('myapp:invoicelist')

    def formset_variants_valid(self, formset):
        """
        Hook for custom formset saving.. useful if you have multiple formsets
        """
        variants = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for variant in variants:
            variant.invoice = self.object
            variant.save()


class InvoiceCreate(InvoiceInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(InvoiceCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'variants': VariantFormSet(prefix='variants'),
                # 'images': ImageFormSet(prefix='images'),
            }
        else:
            return {
                'variants': VariantFormSet(self.request.POST or None, self.request.FILES or None, prefix='variants'),
                # 'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, prefix='images'),
            }


class InvoiceUpdate(InvoiceInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(InvoiceUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'variants': VariantFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object,
                                       prefix='variants'),
            # 'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object,
            #                        prefix='images'),
        }


def delete_variant(request, pk):
    try:
        variant = invoiceitem.objects.get(id=pk)
    except invoiceitem.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('myapp:update_invoice', pk=variant.invoice.id)

    variant.delete()
    messages.success(
            request, 'Variant deleted successfully'
            )
    return redirect('myapp:update_invoice', pk=variant.invoice.id)

