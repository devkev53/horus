from django.urls import path
from cliente.views import ClientesView, CreateClientView, UpdateClientView, deactivateClient

urlpatterns = [
  path('clients/', ClientesView.as_view(), name='clients'),
  path('clients/add/', CreateClientView.as_view(), name='clients_add'),
  path('clients/update/<int:pk>/', UpdateClientView.as_view(), name='clients_update'),
  path('clients/delete/<int:pk>/', deactivateClient, name='clients_delete'),
]
