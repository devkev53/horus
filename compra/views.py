from decimal import Decimal
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from base.views import ListBaseView, CreateBaseView



from catalogo.models import Product

from compra.forms import BuyForm
# Create your views here.



class BuysListView(ListBaseView):
    template_name = "buys/buys_list.html"
    form_class = BuyForm



def buysCreate(request, pk=None):
    pass

class BuyCreateView(CreateBaseView):
    template_name = "buys/buy_form.html"
    model = BuyForm.Meta.model
    form_class = BuyForm
    success_url = reverse_lazy('buys_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            print(request.POST)
            action = request.POST['action']
            if action == 'search_products':
                data = []
                term = request.POST['term']
                if len(term) > 0:
                    products = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
                    for i in products:
                        item = i.toJSON()
                        item['value'] = i.name
                        item['quantity'] = 1
                        item['subtotal'] = Decimal(item['price_sale'] * item['quantity'])
                        data.append(item)
            else:
                data['error'] = 'No se ha ingresado una opcion'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)