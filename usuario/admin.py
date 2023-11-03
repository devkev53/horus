from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from usuario.models import User
from django.contrib.auth.models import Group

# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
  ''' Admin View for User '''

  list_display = (
    'id', 'username', 'reset_token',
    'email', 'get_full_name', 'is_active',
    'is_staff',
  )
  list_display_links = ('id', 'username',)
  search_fields = ('username','name', 'last_name', 'email')
  fieldsets = (
    (None, {'fields': ('email', 'username', 'password')}),

    (_('Información Personal'), {'fields': ( 'name', 'last_name')}),

    (_('Permisos'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',)}),

    (_('Fechas Importantes'), {'fields': ('last_login',)}),
  )