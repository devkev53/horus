from django import forms
from venta.models import Sale, SaleDetail

class SaleForm(forms.ModelForm):
  search_nit = forms.CharField(initial='C/F', max_length=9, required=False)
  cliente = forms.CharField(initial='Consumidor Final', disabled=True, required=False)


  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'w-full bg-gray-50 border border-zinc-300 text-zinc-600 focus:outline-none focus:border-zinc-500 p-1.5 px-2 rounded-lg'
      form.field.widget.attrs['autocomplete'] = 'off'

  class Meta:
    model = Sale
    fields = (
      'search_nit', 'date', 'id', 'client_id', 'cliente',
      'serie', 'dte',
      'authorization_date', 'total',
    )


class SaleDetailForm(forms.ModelForm):
  class Meta:
    model = SaleDetail
    fields = (
      'id', 'sale_id', 'product_id', 'quantity', 'total',
    )