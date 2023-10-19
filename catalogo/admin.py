from django.contrib import admin
from catalogo.models import Category, Product

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  '''Admin View for Category'''

  list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  '''Admin View for Product'''

  list_display = ('id', 'preview_img', 'name', 'price_cost', 'sale_price')
  list_filter = ('category_id',)
  list_display_links = ('id', 'preview_img', 'name',)
  # inlines = [
  #   Inline,
  # ]
  # raw_id_fields = ('',)
  # readonly_fields = ('',)
  search_fields = ('name', 'category_id')
  # date_hierarchy = ''
  # ordering = ('',)