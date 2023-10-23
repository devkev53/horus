from django import forms
from catalogo.models import Category

class CategoryCreateForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ("name",'image')
