from decimal import Decimal
import json
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from base.views import ListBaseView, CreateBaseView, UpdateBaseView, ValidatePermissionRequiredMixin
from django.db import transaction
from django.views.generic.detail import DetailView




from catalogo.models import Product
from catalogo.utils import update_product_stock

from compra.forms import BuyForm, BuyDetailForm, PaymentForm
# Create your views here.


class BuyDetailView(DetailView):
    model = BuyForm.Meta.model
    template_name = 'buys/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deatils"] = BuyDetailForm.Meta.model.objects.filter(buy_id=self.object)
        return context


class BuysListView(ValidatePermissionRequiredMixin, ListBaseView):
    permission_required = ['compra.view_buy',]
    template_name = "buys/buys_list.html"
    form_class = BuyForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            # *-*-*-*-*- SI RECIBE BUSCAR PRODUCTOS *-*-*-*-*-*
            if action == 'searchData':
                data = []
                for i in self.form_class.Meta.model.objects.all():
                    data.append(i.toJSON())

            # *-*-*-*-*- SI RECIBE BUSCAR DETALLE DE PRODUCTOS *-*-*-*-*-*
            elif action == 'search_details':
                data = []
                buy = BuyForm.Meta.model.objects.filter(id=request.POST['id']).get()
                for d in BuyDetailForm.Meta.model.objects.filter(buy_id=buy):
                    data.append(d.toJSON())

            # *-*-*-*-*- SI RECIBE BUSCAR ADD PAY *-*-*-*-*-*
            elif action == 'addPay':
                payment = PaymentForm(data=request.POST)
                if payment.is_valid():
                    payment.save()
                else:
                    data['error'] = payment.errors
                    data['params'] = payment.data
            # *-*-*-*-*- SI RECIBE BUSCAR ADD PAY *-*-*-*-*-*
            elif action == 'search_pays':
                data = []
                for p in PaymentForm.Meta.model.objects.filter(buy_id=request.POST['id'], is_active=True):
                    print(p)
                    data.append(p.toJSON())

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addPayForm'] = PaymentForm
        return context


class BuyCreateView(PermissionRequiredMixin, CreateBaseView):
    permission_required = ('compra.add_buy',)
    template_name = "buys/buy_form.html"
    model = BuyForm.Meta.model
    form_class = BuyForm
    success_url = reverse_lazy('buys_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            # *-*-*-*-*- SI RECIBE BUSCAR PRODUCTOS *-*-*-*-*-*
            if action == 'search_products':
                data = []
                term = request.POST['term']
                if len(term) > 0:
                    products = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
                    for i in products:
                        item = i.toJSON()
                        item['value'] = i.name
                        item['quantity'] = 1
                        item['subtotal'] = Decimal(item['price_sale'] * item['quantity'])
                        data.append(item)

            # *-*-*-*-*- SI RECIBE CREAR COMPRA *-*-*-*-*-*
            elif action == 'add':
                with transaction.atomic():
                    # Transforma el array en JSON
                    buys = json.loads(request.POST['buys'])

                    # Crea el diccionario del encabezado de la compra
                    buy = {
                        "date":buys['date'],
                        "serie":buys['serie'],
                        "reference":buys['reference'],
                        "provider_id":buys['provider_id'],
                        "total": buys['total']
                    }
                    # Pasa los datos del encabezado al formulario
                    instance = self.form_class(data=buy)
                    # Valida si es correcto
                    if instance.is_valid():
                        # Guarda el objecto
                        buy_data = instance.save()
                    else:
                        data['error'] = instance.errors

                    # Tomla el listado de productos de la compra
                    products_list = buys['products']
                    for product in products_list:
                        productDict = {
                            "buy_id":buy_data.id,
                            "product_id":product['id'],
                            "quantity": product['quantity'],
                            "sub_total":Decimal(Decimal(product['subtotal']) * int(product['quantity'])),
                        }
                        detail_instance = BuyDetailForm(data=productDict)
                        if detail_instance.is_valid():
                            detail_instance.save()


                        else:
                            data["error"] = detail_instance.errors


                    # Llama al metodo para aumentar el stock
                    update_product_stock()
            else:
                data['error'] = 'No se ha ingresado una opcion'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class BuyEditView(UpdateBaseView):
    template_name = "buys/buy_edit.html"
    model = BuyForm.Meta.model
    form_class = BuyForm
    success_url = reverse_lazy('buys_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            # *-*-*-*-*- SI RECIBE BUSCAR PRODUCTOS *-*-*-*-*-*
            if action == 'search_products':
                data = []
                term = request.POST['term']
                if len(term) > 0:
                    products = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
                    for i in products:
                        item = i.toJSON()
                        item['value'] = i.name
                        item['quantity'] = 1
                        item['subtotal'] = Decimal(item['price_sale'] * item['quantity'])
                        data.append(item)

            # *-*-*-*-*- SI RECIBE BUSCAR EL LISTADO DE DETALLES DE VENTA *-*-*-*-*-*
            elif action == 'search_details':
                data = []
                buy = BuyForm.Meta.model.objects.filter(id=request.POST['id']).get()
                for d in BuyDetailForm.Meta.model.objects.filter(buy_id=buy):
                    data.append(d.toJSON())

            # *-*-*-*-*- SI RECIBE LA ACCION DE EDITAR COMPRA *-*-*-*-*-*
            elif action == 'edit':
                with transaction.atomic():
                    # Transforma el array en JSON
                    buys = json.loads(request.POST['buys'])

                    # Crea el diccionario del encabezado de la compra
                    buy = {
                        "date":buys['date'],
                        "serie":buys['serie'],
                        "reference":buys['reference'],
                        "provider_id":buys['provider_id'],
                        "total": buys['total']
                    }
                    # Pasa los datos del encabezado al formulario
                    instance = self.form_class(data=buy, instance=self.get_object())
                    # Valida si es correcto
                    if instance.is_valid():
                        # Guarda el objecto
                        buy_data = instance.save()
                    else:
                        data['error'] = instance.errors
                        data['error_in'] = 'Create Buy instance'

                    # Elimina el detalle para actualizar el nuevo
                    buy_data.buydetail_set.all().delete()
                    # Tomla el listado de productos de la compra
                    products_list = buys['products']
                    for product in products_list:
                        productDict = {
                            "buy_id":buy_data.id,
                            "product_id":product['id'],
                            "quantity": product['quantity'],
                            "sub_total":Decimal(Decimal(product['subtotal']) * int(product['quantity'])),
                        }
                        detail_instance = BuyDetailForm(data=productDict)
                        if detail_instance.is_valid():
                            detail_instance.save()

                        else:
                            data["error"] = detail_instance.errors
                            data['error_in'] = detail_instance.data


                    # Llama al metodo para aumentar el stock
                    update_product_stock()

            else:
                data['error'] = 'No se ha ingresado una opcion'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        buy = self.get_object()
        items = []
        query_items = BuyDetailForm.Meta.model.objects.filter(buy_id=buy.id, is_active=True)
        for item in query_items:
            items.append(item)
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


def deactivateBuy(request, pk):
    object = BuyForm.Meta.model.objects.filter(pk=pk).first()
    template_name='buys/buy_delete.html'
    success_url = reverse_lazy('buys_list')
    url_redirect=success_url
    context = {}

    if not object:
        return redirect

    if request.method == 'GET':
        context={'object':object}

    if request.method == 'POST':
        object.is_active = False
        object.save()
        # Llama al metodo para aumentar el stock
        update_product_stock()
        return redirect(url_redirect)

    return render(request, template_name, context)
