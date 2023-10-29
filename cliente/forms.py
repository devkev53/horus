from django import forms
from cliente.models import Client


class ClientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'w-full bg-gray-50 border border-zinc-300 text-zinc-600 focus:outline-none focus:border-zinc-500 p-1.5 px-2 rounded-lg'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Client
        fields = ('id', 'name', 'last_name', 'address', 'phone', 'nit',)
