import datetime
from decimal import Decimal
from json import dumps
from typing import Any
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from catalogo.models import Product
from venta.models import Sale, SaleDetail


months = [
    {'id':1,'name':'Enero'},
    {'id':2,'name':'Febrero'},
    {'id':3,'name':'Marzo'},
    {'id':4,'name':'Abril'},
    {'id':5,'name':'Mayo'},
    {'id':6,'name':'Junio'},
    {'id':7,'name':'Julio'},
    {'id':8,'name':'Agosto'},
    {'id':9,'name':'Septiembre'},
    {'id':10,'name':'Octubre'},
    {'id':11,'name':'Noviembre'},
    {'id':12,'name':'Diciembre'},
]


# Create your views here.

class InicioView(TemplateView):
    template_name = 'public/inicio.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

class ConocenosView(TemplateView):
    template_name = 'public/about.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

class ContactView(TemplateView):
    template_name = 'public/contact.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "base/dashboard.html"
    login_url= '/login'


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}

        try:
            action = request.POST['action']

            if action == 'get_sales':
                data = self.get_sales_year_month()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_total_sale_today(self):
        data = {}
        total = Decimal(0.00)

        try:
            today = datetime.date.today()
            sales = Sale.objects.filter(created=today)
            for sale in sales:
                total += Decimal(sale.total)
            data['sales'] = sales
            data['total'] = format(total, '.2f')
        except Exception as e:
            return e
        return data

    def get_alert_products(self):
        prods = []

        try:
            products = Product.objects.filter(is_active=True).all()
            for prod in products:
                if prod.stock <= prod.show_alert:
                    prods.append(prod)

        except Exception as e:
            return e
        return prods

    def get_then_more_sale(self):
        prods = []
        try:
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            products = Product.objects.filter(is_active=True).all()
            sales = Sale.objects.filter(created__year=year, created__month=month)
            prods = SaleDetail.objects.all().filter(sale_id__in=sales).values(
                'product_id__name', 'product_id__image', 'product_id__price_sale'
            ).annotate(quantity=Sum('quantity')).annotate(total=Sum('total'))[0:9]

        except Exception as e:
            return e
        return prods

    def get_sales_year_month(self):
        data = []
        try:
            year = datetime.datetime.now().year
            for month in months:
                total = 0
                for sale in Sale.objects.filter(created__year=year, created__month=month['id']):
                    total += sale.total
                info = dumps({
                    "label": month['name'],
                    "y": format(total, '.2f')
                })
                data.append(info)
        except Exception as e:
            return e
        return data


    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["get_then_more_sale"] = self.get_then_more_sale()
        context["products_alert"] = self.get_alert_products()
        context["get_total_today"] = self.get_total_sale_today()
        context['get_sales_year_month'] = self.get_sales_year_month()
        context['today'] = datetime.date.today()
        return context



# LOGIN VIEW

class LoginFormView(LoginView):
    template_name = 'base/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('clients')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Iniciar Sesion'
        return context



# CUSTOM BASE VIEWS
class ListBaseView(LoginRequiredMixin, TemplateView):
    login_url= '/login'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.form_class.Meta.model.objects.filter(is_active=True).all()
        context['titulo'] = 'Iniciar Sesion'
        context['instance'] = instance
        return context


class CreateBaseView(LoginRequiredMixin, CreateView):
    login_url= '/login'

    def get_context_data(self, **kwargs):
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        context = super().get_context_data(**kwargs)
        context['lazyUrl'] = self.url_redirect
        return super().get_context_data(**kwargs)


class UpdateBaseView(LoginRequiredMixin, UpdateView):
    login_url= '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lazyUrl'] = self.url_redirect
        return context


class CustomDeleteBaseView(LoginRequiredMixin, UpdateView):
    success_url = '/'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lazyUrl'] = self.url_redirect
        return context