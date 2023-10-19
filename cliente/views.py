from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from cliente.models import Client


# Create your views here.



class ClientesView(TemplateView):
    template_name = "cliente/clientes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = Client.objects.filter(is_active=True).all()
        context['titulo'] = 'Iniciar Sesion'
        context['clients'] = clients
        return context


class CreateClientView(CreateView):
    model=Client
    fields='__all__'