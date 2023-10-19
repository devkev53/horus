from django.shortcuts import render, redirect
from django.views.generic import TemplateView

# Create your views here.



class Sales(TemplateView):
    template_name = "venta/sales.html"
