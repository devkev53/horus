from django import forms
from catalogo.models import Category, Product

class CategoryCreateForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ("name",'image')


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = (
            'name', 'description', 'image', 'category_id',
            'price_cost', 'price_sale', 'provider_id'
            )
        widgets = {
            "category_id": forms.Select(attrs={
                'class': 'w-full bg-gray-50 border border-zinc-300 text-zinc-600 focus:outline-none focus:border-zinc-500 p-2.5 px-2 rounded-lg'
            }),
            "provider_id": forms.Select(attrs={
                'class': 'w-full bg-gray-50 border border-zinc-300 text-zinc-600 focus:outline-none focus:border-zinc-500 p-2.5 px-2 rounded-lg'
            }),
        }
