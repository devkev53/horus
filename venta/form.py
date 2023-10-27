from django import forms
from venta.models import Sale, SaleDetail

class SaleForm(forms.ModelForm):
  class Meta:
    model = Sale
    fields = (
      'id', 'client_id',
      'serie', 'dte',
      'authorization', 'total',
    )


class SaleDetailForm(forms.ModelForm):
  class Meta:
    model = SaleDetail
    fields = (
      'id', 'sale_id', 'product_id', 'quantity', 'total',
    )