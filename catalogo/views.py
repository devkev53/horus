from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from base.views import CreateBaseView, UpdateBaseView, ListBaseView, ValidatePermissionRequiredMixin

from catalogo.forms import CategoryCreateForm, ProductForm

# Create your views here.


class CategoryListView(ListBaseView):
    template_name = "category/category_list.html"
    form_class = CategoryCreateForm


class CategoryCreateView(CreateBaseView):
    template_name='category/category_form.html'
    form_class = CategoryCreateForm
    success_url = reverse_lazy('categories')
    url_redirect = success_url


class CategoryEditView(UpdateBaseView):
    model = CategoryCreateForm.Meta.model
    form_class = CategoryCreateForm
    success_url = reverse_lazy('categories')
    url_redirect = success_url
    template_name = "category/category_update.html"


def deactivateCategory(request, pk):
    object = CategoryCreateForm.Meta.model.objects.filter(pk=pk).first()
    template_name='category/category_delete.html'
    success_url = reverse_lazy('categories')
    url_redirect=success_url
    context = {}

    if not object:
        return redirect

    if request.method == 'GET':
        context={'object':object}

    if request.method == 'POST':
        object.is_active = False
        object.save()
        return redirect(url_redirect)

    return render(request, template_name, context)





class ProductListView(ListBaseView):
    template_name = "products/products_list.html"
    form_class = ProductForm


class ProductCreateView(CreateBaseView):
    template_name='products/products_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('products_list')
    url_redirect = success_url



class ProductEditView(ValidatePermissionRequiredMixin, UpdateBaseView):
    permission_required = ['catalogo.update_product',]
    model = ProductForm.Meta.model
    form_class = ProductForm
    success_url = reverse_lazy('products_list')
    url_redirect = success_url
    template_name = "products/products_update.html"




def deactivateProduct(request, pk):
    object = ProductForm.Meta.model.objects.filter(pk=pk).first()
    template_name='products/products_delete.html'
    success_url = reverse_lazy('categories')
    url_redirect=success_url
    context = {}

    if not object:
        return redirect

    if request.method == 'GET':
        context={'object':object}

    if request.method == 'POST':
        object.is_active = False
        object.save()
        return redirect(url_redirect)

    return render(request, template_name, context)

