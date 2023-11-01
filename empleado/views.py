from typing import Any
from django import http
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from base.views import CreateBaseView, UpdateBaseView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from empleado.forms import EmpleadoForm
from usuario.forms import UserForm


# Create your views here.



class EmpleadosView(LoginRequiredMixin, TemplateView):
    template_name = "empleado/list.html"
    login_url= '/login'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = EmpleadoForm.Meta.model.objects.filter(is_active=True).all()
        context['titulo'] = 'Iniciar Sesion'
        context['instance'] = instance
        return context


class CreateEmployeetView(CreateBaseView):
    form_class = EmpleadoForm
    success_url = reverse_lazy('employees_list')
    template_name = "empleado/add.html"
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
      data = []
      try:
        print(request.POST)
        userDict = {
            'username': request.POST['username'],
            'email': request.POST['email'],
            'name': request.POST['name'],
            'last_name': request.POST['last_name'],
        }
        user_instance = UserForm(data=userDict)
        if user_instance.is_valid():
            user = user_instance.save()
        else:
            data['error'] = user_instance.errors
            return data

        print('*-*-*-*-*- Se Creo el Usuario -*-*-*-*-*-*')
        employeeDict = {
            "user_id": user.pk,
            'address': request.POST['address'],
            'birthday': request.POST['birthday'],
            'salary': request.POST['salary'],
            'start_at_work': request.POST['start_at_work'],
        }
        employee_instance = EmpleadoForm(data=employeeDict)
        if employee_instance.is_valid():
            employee_instance.save()
            return HttpResponseRedirect('/employees')
        else:
            data['error'] = employee_instance.errors
            return data

      except Exception as e:
          data['error'] = str(e)
      return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['userForm'] = UserForm
      return context



class UpdateEmployeeView(UpdateBaseView):
    model = EmpleadoForm.Meta.model
    form_class=EmpleadoForm
    success_url = reverse_lazy('clients')
    url_redirect=success_url
    template_name="empleado/add_update.html"

    def post(self, request, *args, **kwargs):
      data = []
      try:
        print(request.POST)
        userDict = {
            'username': request.POST['username'],
            'email': request.POST['email'],
            'name': request.POST['name'],
            'last_name': request.POST['last_name'],
        }
        user_instance = UserForm(data=userDict)
        if user_instance.is_valid():
            user = user_instance.save()
        else:
            data['error'] = user_instance.errors
            return data

        print('*-*-*-*-*- Se Creo el Usuario -*-*-*-*-*-*')
        employeeDict = {
            "user_id": user.pk,
            'address': request.POST['address'],
            'birthday': request.POST['birthday'],
            'salary': request.POST['salary'],
            'start_at_work': request.POST['start_at_work'],
        }
        employee_instance = EmpleadoForm(data=employeeDict)
        if employee_instance.is_valid():
            employee_instance.save()
            return HttpResponseRedirect('/employees')
        else:
            data['error'] = employee_instance.errors
            return data

      except Exception as e:
          data['error'] = str(e)
      return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['userForm'] = UserForm
      return context



def deactivateEmployee(request, pk):
    object = EmpleadoForm.Meta.model.objects.filter(pk=pk).first()
    template_name='empleado/delete.html'
    success_url = reverse_lazy('employees_list')
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