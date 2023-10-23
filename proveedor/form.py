from django import forms
from proveedor.models import Providers

class ProvidersForm(forms.ModelForm):

  class Meta:
    model = Providers
    fields = (
      'logo', 'company_name', 'reference_contact',
      'address', 'phone', 'nit',
    )