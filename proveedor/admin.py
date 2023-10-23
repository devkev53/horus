from django.contrib import admin
from proveedor.models import Providers

# Register your models here.

@admin.register(Providers)
class ProvidersAdmin(admin.ModelAdmin):
  '''Admin View for Providers'''

  list_display = ('id', 'company_name', 'reference_contact', 'phone', 'address','nit')
  # list_filter = ('',)
  # inlines = [
  #   Inline,
  # ]
  # raw_id_fields = ('',)
  # readonly_fields = ('',)
  search_fields = ('company_name', 'reference_contact', 'phone', 'nit')
  # date_hierarchy = ''
  # ordering = ('',)
