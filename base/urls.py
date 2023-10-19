from django.urls import path
from base.views import LoginFormView, DashboardView
from django.contrib.auth.views import LogoutView

urlpatterns = [
  path('login/', LoginFormView.as_view(), name='login'),
  path('', DashboardView.as_view(), name='dashboard'),
  path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
