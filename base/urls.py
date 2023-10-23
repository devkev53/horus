from django.urls import path
from base.views import LoginFormView, DashboardView
from django.contrib.auth import views as auth_views

urlpatterns = [
  path('login/', auth_views.LoginView.as_view(template_name ='base/login.html'), name='login'),
  path('', DashboardView.as_view(), name='dashboard'),
  path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
