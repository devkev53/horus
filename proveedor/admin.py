from django.contrib import admin
from proveedor.models import Supplier

# Register your models here.

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
  '''Admin View for Supplier'''

  list_display = ('id', 'company_name', 'reference_contact', 'phone', 'address')
  # list_filter = ('',)
  # inlines = [
  #   Inline,
  # ]
  # raw_id_fields = ('',)
  # readonly_fields = ('',)
  search_fields = ('company_name', 'reference_contact', 'phone')
  # date_hierarchy = ''
  # ordering = ('',)
