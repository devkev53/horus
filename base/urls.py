from django.urls import path
from base.views import LoginFormView, DashboardView, InicioView, ConocenosView, ContactView
from django.contrib.auth import views as auth_views

urlpatterns = [
  path('inicio/', InicioView.as_view(), name='inicio'),
  path('conocenos/', ConocenosView.as_view(), name='conocenos'),
  path('contacto/', ContactView.as_view(), name='contact'),
  path('login/', auth_views.LoginView.as_view(template_name ='base/login.html'), name='login'),
  path('', DashboardView.as_view(), name='dashboard'),
  path('logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),
]
