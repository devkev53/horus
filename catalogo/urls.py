from django.urls import path
from catalogo.views import CategoryListView, CategoryCreateView, \
  CategoryEditView, deactivateCategory, ProductListView, ProductCreateView, deactivateProduct, ProductEditView

urlpatterns = [
  path('categories/', CategoryListView.as_view(), name='categories'),
  path('category/add/', CategoryCreateView.as_view(), name='category_add'),
  path('category/<int:pk>', CategoryEditView.as_view(), name='category_edit'),
  path('category/delete/<int:pk>', deactivateCategory, name='category_delete'),

  # Products PATHS
  path('products/', ProductListView.as_view(), name='products_list'),
  path('products/add/', ProductCreateView.as_view(), name='products_add'),
  path('products/<int:pk>', ProductEditView.as_view(), name='products_edit'),
  path('products/delete/<int:pk>', deactivateProduct, name='products_delete'),
]
