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
from django.db import transaction
import json


from empleado.forms import EmpleadoForm, EmpleadoUpdateForm
from usuario.forms import UserForm, UserUpdateForm


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

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            # *-*-*-*-*- SI RECIBE CREAR VENTA *-*-*-*-*-*
            if action == 'add':
                with transaction.atomic():
                    # Transforma el array en JSON

                    # Crea el diccionario del encabezado de la compra
                    userDict = {
                        "username":request.POST['username'],
                        "email":request.POST['email'],
                        "name":request.POST['name'],
                        "last_name": request.POST['last_name'],
                        "password":request.POST['password'],
                    }
                    # Pasa los datos del encabezado al formulario
                    instance = UserForm(data=userDict)
                    # Valida si es correcto
                    if instance.is_valid():
                        # Guarda el objecto
                        user_data = instance.save()
                    else:
                        data['user'] = instance.data
                        data['error'] = instance.errors

                    employeeDict = {
                        "user_id": user_data.id,
                        'address': request.POST['address'],
                        'salary': request.POST['salary'],
                        'birthday': request.POST['birthday'],
                        'start_at_work': request.POST['start_at_work'],
                    }

                    employee_instance = EmpleadoForm(data=employeeDict)
                    if employee_instance.is_valid():
                        employee_instance.save()
                    else:
                        data['employee'] = employee_instance.data
                        data['error_employee'] = employee_instance.errors

            else:
                data['error'] = 'No se ha ingresado una opcion'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserForm
        return context



class UpdateEmployeeView(UpdateBaseView):
    model = EmpleadoForm.Meta.model
    form_class=EmpleadoForm
    success_url = reverse_lazy('employees_list')
    url_redirect=success_url
    template_name="empleado/add_update.html"

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            # *-*-*-*-*- SI RECIBE CREAR VENTA *-*-*-*-*-*
            if action == 'edit':
                with transaction.atomic():
                    # Transforma el array en JSON

                    # Crea el diccionario del encabezado de la compra
                    userDict = {
                        "name":request.POST['name'],
                        "last_name": request.POST['last_name'],
                    }
                    # Pasa los datos del encabezado al formulario
                    print(self.get_object())
                    instance = UserUpdateForm(data=userDict, instance=self.get_object())
                    # Valida si es correcto
                    if instance.is_valid():
                        # Guarda el objecto
                        user_data = instance.save()
                    else:
                        data['user'] = instance.data
                        data['error'] = instance.errors
                        data['employee_errors'] = 'El error esta en el usuario'

                    birthday = request.POST['birthday']
                    start_at_work = request.POST['start_at_work']

                    if birthday == '':
                        birthday = None

                    if start_at_work == '':
                        start_at_work = None

                    employeeDict = {
                        "user_id": user_data.id,
                        'address': request.POST['address'],
                        'salary': request.POST['salary'],
                        'birthday': birthday,
                        'start_at_work': start_at_work,
                    }
                    print(user_data.id)
                    old_employe_instance = EmpleadoUpdateForm.Meta.model.objects.filter(pk=self.kwargs['pk'])
                    employee_form = EmpleadoUpdateForm(data=employeeDict)
                    old_employe_instance.update(
                        address=employee_form.data['address'],
                        birthday=employee_form.data['birthday'],
                        salary=employee_form.data['salary'],
                        start_at_work=employee_form.data['start_at_work'],
                    )
            else:
                data['error'] = 'No se ha ingresado una opcion'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.get_object()
        context['user_form'] = UserForm
        context['user_object'] = UserForm.Meta.model.objects.filter(id=employee.user_id.id).get()
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