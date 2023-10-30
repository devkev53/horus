from django.contrib import admin
from catalogo.models import Category, Product

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  '''Admin View for Category'''

  list_display = ('id', 'name', 'image', 'get_url_img')



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  '''Admin View for Product'''

  list_display = ('id', 'preview_img', 'name', 'stock')
  list_filter = ('category_id',)
  list_display_links = ('preview_img', 'name',)
  search_fields = ('name', 'category_id__name')
