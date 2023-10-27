from django.urls import path
from venta.views import SaleListView, SaleCreateView

urlpatterns = [
  path('sales/', SaleListView.as_view(), name='sales_list'),
  path('sales/add', SaleCreateView.as_view(), name='sales_add'),
]
