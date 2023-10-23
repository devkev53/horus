from django.urls import path
from catalogo.views import CategoryListView, CategoryCreateView, CategoryEditView, deactivateCategory

urlpatterns = [
  path('categories/', CategoryListView.as_view(), name='categories'),
  path('category/add/', CategoryCreateView.as_view(), name='category_add'),
  path('category/<int:pk>', CategoryEditView.as_view(), name='category_edit'),
  path('category/delete/<int:pk>', deactivateCategory, name='category_delete'),
]
