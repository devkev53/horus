from django.forms import forms
from cliente.models import Client


class Form(forms.ModelForm):

    class Meta:
        model = Client
        fields = "__all__"
