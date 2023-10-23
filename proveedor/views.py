from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from base.views import ListBaseView, CreateBaseView, UpdateBaseView
from proveedor.form import ProvidersForm

# Create your views here.


class ProvidersListView(ListBaseView):
  template_name = "providers/providers_list.html"
  form_class = ProvidersForm


class ProvidersCreateView(CreateBaseView):
  template_name='providers/provider_form.html'
  form_class = ProvidersForm
  success_url = reverse_lazy('providers_list')
  url_redirect = success_url

class ProviderEditView(UpdateBaseView):
    model = ProvidersForm.Meta.model
    form_class = ProvidersForm
    success_url = reverse_lazy('providers_list')
    url_redirect = success_url
    template_name = "providers/provider_update.html"


def deactivateProvider(request, pk):
    object = ProvidersForm.Meta.model.objects.filter(pk=pk).first()
    template_name='providers/provider_delete.html'
    success_url = reverse_lazy('providers_list')
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