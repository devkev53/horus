from django.urls import path
from empleado.views import EmpleadosView, CreateEmployeetView,deactivateEmployee, UpdateEmployeeView

urlpatterns = [
    path('employees/', EmpleadosView.as_view(), name='employees_list'),
    path('employees/update/<int:pk>', UpdateEmployeeView.as_view(), name='employees_list'),
    path('employees/add/', CreateEmployeetView.as_view(), name='employees_add'),
    path('employees/delete/<int:pk>', deactivateEmployee, name='employees_del'),
]
