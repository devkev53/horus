from django.urls import path
from venta.views import SaleListView

urlpatterns = [
  path('sales/', SaleListView.as_view(), name='sales_list'),
]
