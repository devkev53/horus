from django.contrib import admin
from cliente.models import Client

# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
  '''Admin View for Client'''

  list_display = (
    'id', 'get_full_name', 'nit', 'phone', 'address', 'is_active'
  )
  # list_filter = ('',)
  # inlines = [
  #   Inline,
  # ]
  # raw_id_fields = ('',)
  # readonly_fields = ('',)
  search_fields = ('name','last_name', 'nit')
  # date_hierarchy = ''
  # ordering = ('',)