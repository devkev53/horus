from django.urls import path
from compra.views import BuysListView, BuyCreateView, BuyEditView, deactivateBuy, BuyDetailView

urlpatterns = [
    path('buys/detail/<int:pk>', BuyDetailView.as_view(), name='buy_detail'),
    path('buys/', BuysListView.as_view(), name='buys_list'),
    path('buys/add/', BuyCreateView.as_view(), name='buy_add'),
    path('buys/<int:pk>/', BuyEditView.as_view(), name='buy_edit'),
    path('buys/delete/<int:pk>/', deactivateBuy, name='buy_delete'),
]
