from django.urls import path
from venta.views import SaleListView, SaleCreateView, deactivateSale, SaleEditView, InvoicePDF

urlpatterns = [
  path('sales/', SaleListView.as_view(), name='sales_list'),
  path('sales/<int:pk>', SaleEditView.as_view(), name='sales_edit'),
  path('sales/add', SaleCreateView.as_view(), name='sales_add'),
  path('sales/delete/<int:pk>', deactivateSale, name='sales_delete'),
  path('sales/invoice/<int:pk>', InvoicePDF.as_view(), name='invoice')
]
