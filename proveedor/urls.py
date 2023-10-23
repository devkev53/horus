from django.urls import path
from proveedor.views import ProvidersListView, ProvidersCreateView, ProviderEditView, deactivateProvider

urlpatterns = [
    path('providers/', ProvidersListView.as_view(), name='providers_list'),
    path('providers/add/', ProvidersCreateView.as_view(), name='providers_add'),
    path('providers/<int:pk>/', ProviderEditView.as_view(), name='providers_update'),
    path('providers/delete/<int:pk>/', deactivateProvider, name='providers_delete'),
]
