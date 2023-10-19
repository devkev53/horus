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
from base.views import CreateBaseView


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

