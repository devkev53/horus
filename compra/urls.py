from django.urls import path
from compra.views import BuysListView, BuyCreateView, buysCreate

urlpatterns = [
    path('buys/', BuysListView.as_view(), name='buys_list'),
    path('buys/add/', BuyCreateView.as_view(), name='buy_add'),
]
