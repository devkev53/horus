from django.contrib import admin
from compra.models import Buy, BuyDetail, Payment

# Register your models here.


@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
  '''Admin View for Buy'''

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



@admin.register(BuyDetail)
class BuyDetailAdmin(admin.ModelAdmin):
  '''Admin View for BuyDetail'''

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



@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
  '''Admin View for Payment'''

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