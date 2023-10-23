from typing import Any
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



# Create your views here.


class ListBaseView(LoginRequiredMixin, TemplateView):
    login_url= '/login'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.form_class.Meta.model.objects.filter(is_active=True).all()
        context['titulo'] = 'Iniciar Sesion'
        context['instance'] = instance
        return context


class LoginFormView(LoginView):
    template_name = 'base/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('clients')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Iniciar Sesion'
        return context



class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "base/dashboard.html"
    login_url= '/login'



# BASE VIEWS

class CreateBaseView(LoginRequiredMixin, CreateView):
    login_url= '/login'

    def get_context_data(self, **kwargs):
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        context = super().get_context_data(**kwargs)
        context['lazyUrl'] = self.url_redirect
        return super().get_context_data(**kwargs)


class UpdateBaseView(LoginRequiredMixin, UpdateView):
    login_url= '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lazyUrl'] = self.url_redirect
        return context


class CustomDeleteBaseView(LoginRequiredMixin, UpdateView):
    success_url = '/'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lazyUrl'] = self.url_redirect
        return context