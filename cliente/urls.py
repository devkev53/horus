from django.urls import path
from cliente.views import ClientesView, CreateClientView

urlpatterns = [
  path('clients/', ClientesView.as_view(), name='clients'),
  path('clients/add/', CreateClientView.as_view(), name='clients_add'),
]
