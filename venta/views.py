import datetime
from decimal import Decimal
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from base.views import ListBaseView, CreateBaseView, UpdateBaseView
from django.db import transaction
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string, get_template
from django.views.generic.detail import DetailView

from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

from venta.form import SaleForm, SaleDetailForm
from catalogo.forms import ProductForm
from catalogo.utils import update_product_stock
from cliente.forms import ClientForm
# Create your views here.


class SaleDetailView(DetailView):
    model = SaleForm.Meta.model
    template_name = 'sales/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deatils"] = SaleDetailForm.Meta.model.objects.filter(sale_id=self.object)
        context["history"] = self.object.history.all()
        return context

class InvoicePDF(LoginRequiredMixin, DetailView):
    template_name = "sales/invoice_pdf.html"
    login_url= '/login'


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk=None, *args, **kwargs):
        data = {}

        try:
            sale = SaleForm.Meta.model.objects.filter(pk=pk).get()
            details = SaleDetailForm.Meta.model.objects.filter(sale_id__pk=pk).all()

            template = get_template('sales/invoice_pdf.html')
            context = {
                'sale': sale,
                'details': details,
                'now': datetime.datetime.now()
            }

            # html = template.render(context)
            html = render_to_string('sales/invoice_pdf.html', context)
            # css_url = ''
            response = HttpResponse(content_type='application/pdf')
            response["Content-Disposition"] = "inline; report.pdf"

            font_config=FontConfiguration()
            HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config)

            return response
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class SaleListView(ListBaseView):
    template_name = "sales/sales_list.html"
    form_class = SaleForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            # *-*-*-*-*- SI RECIBE BUSCAR LA DATA ENVIA EL LISTADO DE VENTAS *-*-*-*-*-*
            if action == 'searchData':
                data = []
                for i in self.form_class.Meta.model.objects.filter(is_active=True).all():
                    data.append(i.toJSON())


            # *-*-*-*-*- SI RECIBE BUSCAR DETALLES ENVIA EL LISTADO DE DETALLES *-*-*-*-*-*
            elif action == 'search_details':
                data = []
                sale = SaleForm.Meta.model.objects.filter(id=request.POST['id']).get()
                for d in SaleDetailForm.Meta.model.objects.filter(sale_id=sale):
                    data.append(d.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class SaleCreateView(CreateBaseView):
    template_name = "sales/sales_form.html"
    model = SaleForm.Meta.model
    form_class = SaleForm
    success_url = reverse_lazy('sales_list')
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
                    products = ProductForm.Meta.model.objects.filter(name__icontains=request.POST['term'], is_active=True, stock__gt=0)[0:10]
                    for i in products:
                        item = i.toJSON()
                        item['value'] = i.name
                        item['quantity'] = 1
                        item['subtotal'] = Decimal(item['price_sale'] * item['quantity'])
                        data.append(item)

            # *-*-*-*-*- SI RECIBE BUSCAR CLIENTE *-*-*-*-*-*
            elif action == 'search_client':
                nit = request.POST['nit']
                client = ClientForm.Meta.model.objects.filter(nit=nit, is_active=True).first()
                if client is not None:
                    data = client.toJSON()
                else:
                    data['error'] = 'not found'

            # *-*-*-*-*- SI RECIBE CREAR CLIENTE *-*-*-*-*-*
            elif action == 'create_client':
                with transaction.atomic():
                    client_instance = ClientForm(data=request.POST)
                    if client_instance.is_valid():
                        client_created = client_instance.save()
                        data=client_created.toJSON()
                    else:
                        data['error'] = client_instance.errors

            # *-*-*-*-*- SI RECIBE CREAR VENTA *-*-*-*-*-*
            elif action == 'add':
                with transaction.atomic():
                    # Transforma el array en JSON
                    sale = json.loads(request.POST['sale'])

                    # Crea el diccionario del encabezado de la compra
                    saleDict = {
                        "date":sale['date'],
                        "serie":sale['serie'],
                        "dte":sale['dte'],
                        "authorization_date": sale['authorization_date'],
                        "client_id":sale['client_id'],
                        "subtotal": sale['subtotal'],
                        "discount": sale['discount'],
                        "total": sale['total']
                    }
                    # Pasa los datos del encabezado al formulario
                    instance = self.form_class(data=saleDict)
                    # Valida si es correcto
                    if instance.is_valid():
                        # Guarda el objecto
                        sale_data = instance.save()
                    else:
                        data['sale'] = instance.data
                        data['error'] = instance.errors

                    # Tomla el listado de productos de la compra
                    products_list = sale['products']
                    for product in products_list:
                        productDict = {
                            "sale_id":sale_data.id,
                            "product_id":product['id'],
                            "quantity": product['quantity'],
                            "total":Decimal(Decimal(product['subtotal']) * int(product['quantity'])),
                        }
                        detail_instance = SaleDetailForm(data=productDict)
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
        context['client_form'] = ClientForm
        return context


class SaleEditView(UpdateBaseView):
    template_name = "sales/sales_edit.html"
    model = SaleForm.Meta.model
    form_class = SaleForm
    success_url = reverse_lazy('sales_list')
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
                    products = ProductForm.Meta.model.objects.filter(name__icontains=request.POST['term'])[0:10]
                    for i in products:
                        item = i.toJSON()
                        item['value'] = i.name
                        item['quantity'] = 1
                        item['subtotal'] = Decimal(item['price_sale'] * item['quantity'])
                        data.append(item)

            # *-*-*-*-*- SI RECIBE BUSCAR CLIENTE *-*-*-*-*-*
            elif action == 'search_client':
                nit = request.POST['nit']
                client = ClientForm.Meta.model.objects.filter(nit=nit, is_active=True).first()
                if client is not None:
                    data = client.toJSON()
                else:
                    data['error'] = 'not found'

            # *-*-*-*-*- SI RECIBE BUSCAR EL LISTADO DE DETALLES DE VENTA *-*-*-*-*-*
            elif action == 'search_details':
                data = []
                sale = SaleForm.Meta.model.objects.filter(id=request.POST['id']).get()
                for d in SaleDetailForm.Meta.model.objects.filter(sale_id=sale):
                    data.append(d.toJSON())

            # *-*-*-*-*- SI RECIBE LA ACCION DE EDITAR VENTA *-*-*-*-*-*
            elif action == 'edit':
                with transaction.atomic():
                    # Transforma el array en JSON
                    sale = json.loads(request.POST['sale'])

                    # Crea el diccionario del encabezado de la compra
                    saleDict = {
                        "date":sale['date'],
                        "serie":sale['serie'],
                        "dte":sale['dte'],
                        "authorization_date": sale['authorization_date'],
                        "client_id":sale['client_id'],
                        "subtotal": sale['subtotal'],
                        "discount": sale['discount'],
                        "total": sale['total']
                    }
                    # Pasa los datos del encabezado al formulario
                    instance_sale = self.form_class(data=saleDict, instance=self.get_object())
                    # Valida si es correcto
                    if instance_sale.is_valid():
                        # Guarda el objecto
                        sale_edit = instance_sale.save()
                    else:
                        data['error'] = instance_sale.errors
                        data['error_in'] = 'Update Sale Error'

                    # Elimina el detalle para actualizar el nuevo
                    sale_edit.saledetail_set.all().delete()
                    # Tomla el listado de productos de la compra
                    products_list = sale['products']
                    for product in products_list:
                        productDict = {
                            "sale_id":sale_edit.id,
                            "product_id":product['id'],
                            "quantity": product['quantity'],
                            "total":Decimal(product['subtotal']),
                        }
                        detail_instance = SaleDetailForm(data=productDict)
                        if detail_instance.is_valid():
                            detail_instance.save()
                        else:
                            data["error"] = detail_instance.errors
                            data['data'] = detail_instance.data

                    # Llama al metodo para aumentar el stock
                    update_product_stock()
            else:
                data['error'] = 'No se ha ingresado una opcion'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sale = self.get_object()
        items = []
        query_items = SaleDetailForm.Meta.model.objects.filter(sale_id=sale.id)
        for item in query_items:
            items.append(item)
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

def deactivateSale(request, pk):
    object = SaleForm.Meta.model.objects.filter(pk=pk).first()
    template_name='sales/sale_delete.html'
    success_url = reverse_lazy('sale_list')
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


