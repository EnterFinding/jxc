from django.shortcuts import render, HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.core.serializers.json import DjangoJSONEncoder,json
from django import forms

from sale.models import Transfer, Stock, Commdity, TemplateCategory, Patch
from sale.forms import TransferForm, PatchForm
# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        kwargs['form_title'] = TemplateCategory.objects.filter(parent=None)
        return super(IndexView, self).get_context_data(**kwargs)

class TransferView(FormView):
    template_name = 'transfer.html'
    model = Transfer
    success_url = '/'
    form_class = TransferForm
    context_object_name = 'forms'

    def get_context_data(self, **kwargs):
        kwargs['form_title'] = TemplateCategory.objects.filter(parent=None)
        return super(TransferView, self).get_context_data(**kwargs)

    def get_initial(self):
        kwargs = super(TransferView, self).get_initial()
        status = self.kwargs.get('status', None)
        kwargs['transfer_status'] = status
        kwargs['transfer_off'] = 1
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super(TransferView, self).form_valid(form)


    def get(self, request, *args, **kwargs):
        code = kwargs.get('code', None)
        patch = kwargs.get('patch', None)
        if not code:
            return super(TransferView, self).get(request, *args, **kwargs)
        data = Stock.objects.filter(stock_code__commdity_code=code).distinct().values('stock_patch__patch_code')
        if patch and code:
            data = Stock.objects.filter(stock_code__commdity_code=code, stock_patch__patch_code=patch).values('stock_code__commdity_name', 'stock_code__commdity_mod__mod_name', 'stock_code__commdity_price', 'stock_patch__patch_product', 'stock_patch__patch_validity')
        return HttpResponse(json.dumps(list(data), cls=DjangoJSONEncoder), content_type='application/json')

class PatchView(FormView):
    template_name = 'patch.html'
    model = Patch
    success_url = '/'
    form_class = PatchForm
    context_object_name = 'form'
    
    def get_initial(self):
        kwargs = super(PatchView, self).get_initial()
        print(self.kwargs)
        kwargs['patch_commdity'] = self.kwargs.get('code')
        return kwargs
    
    def form_invalid(self, form):
        kwargs = super(PatchView, self).form_invalid(form)
        print(form.errors)
        return kwargs