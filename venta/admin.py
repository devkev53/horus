from django.contrib import admin
from venta.models import Sale, SaleDetail

# Register your models here.


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
  '''Admin View for Sale'''

  list_display = ('date', 'authorization_date', 'client_id', 'is_active', 'total')
  # list_filter = ('',)
  # inlines = [
  #   Inline,
  # ]
  # raw_id_fields = ('',)
  # readonly_fields = ('',)
  # search_fields = ('',)
  # date_hierarchy = ''
  # ordering = ('',)



@admin.register(SaleDetail)
class SaleDetailAdmin(admin.ModelAdmin):
  '''Admin View for SaleDetail'''

  list_display = ('sale_id', 'product_id', 'quantity', 'total',)
  # list_filter = ('',)
  # inlines = [
  #   Inline,
  # ]
  # raw_id_fields = ('',)
  # readonly_fields = ('',)
  # search_fields = ('',)
  # date_hierarchy = ''
  # ordering = ('',)