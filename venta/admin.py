from django.contrib import admin
from venta.models import Sale, SaleDetail

# Register your models here.


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
  '''Admin View for Sale'''

  # list_display = ('',)
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

  # list_display = ('',)
  # list_filter = ('',)
  # inlines = [
  #   Inline,
  # ]
  # raw_id_fields = ('',)
  # readonly_fields = ('',)
  # search_fields = ('',)
  # date_hierarchy = ''
  # ordering = ('',)