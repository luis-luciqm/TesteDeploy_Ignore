from collections import namedtuple
from django.db.models.query_utils import subclasses
from django.http.response import Http404
from django.views.generic.base import TemplateView, View

from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.list import ListView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render

from .forms import *
from authentication.models import *
from django.views.generic import DetailView
from django.http import JsonResponse
from django.contrib.auth.views import PasswordResetView
from product.models import *
from rolepermissions.mixins import HasRoleMixin

from django.db.models import Count

class DashboardView(LoginRequiredMixin,TemplateView):
    context_object_name = 'queryset'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        users = User.objects.all()
        products = Product.objects.all()
        all_products = Product.objects.all()
        
        context = super().get_context_data(**kwargs)
        context['qtd_users'] = users.count()
        context['qtd_products'] = products.filter(status = 'ACTIVE').count()
        context['last_product'] = all_products.order_by('-created_at')[:6]
        context['all_stores'] = Store.objects.all()[:10]
        context['products'] = Product.objects.all()
        context['products_reports'] = Report_Problem.objects.filter(checked = False).values('product').annotate(dcount = Count('product')).count()
        
        
        context['numbers_stores'] = Product.objects.values('store').annotate(dcount = Count('store'))
        for x in context['numbers_stores']:
            x['porcem'] = int(((100 * x['dcount']) / all_products.count()))
        return context 
    
class StoreCreateView(HasRoleMixin,CreateView):
    model = Store
    fields = '__all__'
    allowed_roles = 'administrador'
    success_url = '/gerenciamento/lista_lojas'
    template_name = 'store_form2.html'
    
class StoreEditView(LoginRequiredMixin,UpdateView):
    model = Store
    fields = '__all__'
    success_url = '/gerenciamento/lista_lojas'
    template_name = 'store_form2.html'

class StoreListView(HasRoleMixin,LoginRequiredMixin,ListView): # ESSE AQUI
    context_object_name = 'queryset'
    template_name = 'store_list.html'
    paginate_by = 1
    model = Store
    allowed_roles = 'administrador'

    def get_context_data(self, **kwargs):
        stores = Store.objects.all()
        context = super().get_context_data(**kwargs)
        context['stores'] = stores
        return context
    
class StoreDisableView(LoginRequiredMixin, ListView):   
    template_name = 'store_list.html'
    context_object_name = 'queryset'
    
    def get_queryset(self):
        store = Store.objects.get(pk=self.kwargs['pk'])
        store.active = False
        store.save()
        return store
    
    def get_context_data(self, **kwargs):
        stores = Store.objects.all()
        context = super().get_context_data(**kwargs)
        context['stores'] = stores
        return context

class StoreActivateView(LoginRequiredMixin, ListView):
    template_name = 'store_list.html'
    context_object_name = 'queryset'
    
    def get_queryset(self):
        store = Store.objects.get(pk=self.kwargs['pk'])
        store.active = True
        store.save()
        return store

    def get_context_data(self, **kwargs):
        stores = Store.objects.all()
        context = super().get_context_data(**kwargs)
        context['stores'] = stores
        return context

class FuncListView(HasRoleMixin,LoginRequiredMixin, ListView):
    context_object_name = 'queryset'
    template_name = 'listUser.html'
    paginate_by = 1
    model = User
    allowed_roles = 'administrador'

    def get_context_data(self, **kwargs):
        users = User.objects.filter(groups__name__in=['funcionario'])
        context = super().get_context_data(**kwargs)
        context['users'] = users
        
        return context

class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'phone', 'email', 'image']
    success_url = '/gerenciamento'
    template_name = 'editUser.html'

class UserDisableView(LoginRequiredMixin, ListView):
    template_name = 'listUser.html'
    context_object_name = 'queryset'

    def get_queryset(self):
        user = User.objects.get(pk=self.kwargs['pk'])
        user.is_active = False
        user.save()
        return user
    
    def get_context_data(self, **kwargs):
        users = User.objects.filter(groups__name__in=['funcionario'])
        context = super().get_context_data(**kwargs)
        context['users'] = users
        
        return context

class UserEnableView(LoginRequiredMixin, ListView):
    template_name = 'listUser.html'
    context_object_name = 'queryset'

    def get_queryset(self):
        user = User.objects.get(pk=self.kwargs['pk'])
        user.is_active = True
        user.save()
        return user
    
    def get_context_data(self, **kwargs):
        users = User.objects.filter(groups__name__in=['funcionario'])
        context = super().get_context_data(**kwargs)
        context['users'] = users
        
        return context

def get_categoria_ajax(request):
    data=[]
    if request.method == "POST":
        categoria_id = request.POST['category_id']
        try:
            subcategorias = SubCategory.objects.filter(category = categoria_id)
   
        except Exception as e: 
            print(e)
            return JsonResponse(data, safe=False)
        return JsonResponse(list(subcategorias.values('id', 'name')), safe = False) 
    
