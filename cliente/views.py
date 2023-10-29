from typing import Any
from django import http
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from base.views import CreateBaseView, UpdateBaseView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from cliente.models import Client
from cliente.forms import ClientForm


# Create your views here.



class ClientesView(LoginRequiredMixin, TemplateView):
    template_name = "cliente/clientes.html"
    login_url= '/login'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = Client.objects.filter(is_active=True).all()
        context['titulo'] = 'Iniciar Sesion'
        context['clients'] = clients
        return context


class CreateClientView(CreateBaseView):
    model=Client
    form_class = ClientForm
    success_url = reverse_lazy('clients')
    url_redirect = success_url



class UpdateClientView(UpdateBaseView):
    model=Client
    form_class=ClientForm
    success_url = reverse_lazy('clients')
    url_redirect=success_url
    template_name_suffix="_update"



def deactivateClient(request, pk):
    object = Client.objects.filter(pk=pk).first()
    template_name='cliente/cliente_delete.html'
    success_url = reverse_lazy('clients')
    url_redirect=success_url
    context = {}

    if not object:
        return redirect

    if request.method == 'GET':
        context={'object':object}

    if request.method == 'POST':
        object.is_active = False
        object.save()
        return redirect(url_redirect)

    return render(request, template_name, context)

@csrf_exempt
def getClientDataByNit(request, pk=None):

    if request.method =='POST':
        data = {}
        try:
            nit = request.POST['nit']
            client = ClientForm.Meta.model.objects.filter(nit=nit, is_active=True).first()
            if client is not None:
                print(client)
                data = client.toJSON()
            else:
                data['error'] = 'not found'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
