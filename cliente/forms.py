from django import forms
from cliente.models import Client


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('name', 'last_name', 'address', 'phone', 'nit',)
