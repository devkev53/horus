from compra.models import Buy, BuyDetail
from venta.models import Sale, SaleDetail
from catalogo.models import Product



# *--*-*-*-*-*- UTIL METHOD FOR ADD BUY INCREMENT STOCK *--*-*-*-*-*-
def update_product_stock():
    for product in Product.objects.all():
      stock = 0
      for buy in Buy.objects.filter(is_active=True):
        for detail in BuyDetail.objects.filter(buy_id=buy):
          if detail.product_id.pk == product.pk:
            stock += detail.quantity

      # DECREMENT STOC FOR SALE
      for sale in Sale.objects.filter(is_active=True):
        for detail in SaleDetail.objects.filter(sale_id=sale):
          if detail.product_id.pk == product.pk:
            stock -= detail.quantity

      product.stock = stock
      print(product)
      product.save()


# *--*-*-*-*-*- UTIL METHOD FOR ADD BUY INCREMENT STOCK *--*-*-*-*-*-
def addBuy_edit_stock(buy):
  for det in BuyDetail.objects.filter(buy_id=buy):
    prod = Product.objects.filter(pk=det.product_id.id).get()
    if det.product_id == prod:
      prod.stock += det.quantity
      prod.save()


# *--*-*-*-*-*- UTIL METHOD FOR DELETE DETAIL BUY DECREMENT STOCK *--*-*-*-*-*-
def delete_BuyDetail_edit_stock(det):
  prod = Product.objects.filter(pk=det.product_id.id).get()
  if det.product_id == prod:
    print(det.quantity)
    if prod.stock >= 0 or prod.stock >= det.quantity:
      new_stock = prod.stock - det.quantity
      print('El Stock luego de borrar es de: {}'.format(new_stock))
      prod.stock = new_stock
      prod.save()

# *--*-*-*-*-*- UTIL METHOD FOR DEACTIVATE BUY DECREMENT STOCK *--*-*-*-*-*-
def deactivate_buy_edit_stock(buy):
  for det in BuyDetail.object.filter(buy_id=buy):
    prod = Product.objects.filter(pk=det.product_id.id).get()
    if det.product_id == prod:
      print(det.quantity)
      if prod.stock >= 0 or prod.stock >= det.quantity:
        new_stock = prod.stock - det.quantity
        print('El Stock luego de borrar es de: {}'.format(new_stock))
        prod.stock = new_stock
        prod.save()


# *--*-*-*-*-*- UTIL METHOD FOR ADD BUY DECREMENT STOCK *--*-*-*-*-*-
def addSale_edit_stock(sale):
  for det in SaleDetail.objects.filter(sale_id=sale):
    prod = Product.objects.filter(pk=det.product_id.id).get()
    if det.product_id == prod:
      prod.stock -= det.quantity
      prod.save()

# *--*-*-*-*-*- UTIL METHOD FOR DELETE DETAIL SALE INCREMENT STOCK *--*-*-*-*-*-
def delete_SaleDetail_edit_stock(det):
  prod = Product.objects.filter(pk=det.product_id.id).get()
  if det.product_id == prod:
    print(prod.name)
    new_stock = prod.stock + det.quantity
    print('El Stock luego de borrar es de: {}'.format(new_stock))
    prod.stock = new_stock
    prod.save()


# *--*-*-*-*-*- UTIL METHOD FOR DEACTIVATE SALE INCREMENT STOCK *--*-*-*-*-*-
def deactivate_sale_edit_stock(sale):
  for det in SaleDetail.objects.filter(sale_id=sale):
    prod = Product.objects.filter(pk=det.product_id.id).get()
    if det.product_id == prod:
      print(det.quantity)
      if prod.stock >= 0 or prod.stock >= det.quantity:
        new_stock = prod.stock + det.quantity
        print('El Stock luego de borrar es de: {}'.format(new_stock))
        prod.stock = new_stock
        prod.save()


# *--*-*-*-*-*- UTIL METHOD FOR ACTIVATE SALE DECREMENT STOCK *--*-*-*-*-*-
def activate_sale_edit_stock(sale):
  for det in SaleDetail.objects.filter(sale_id=sale):
    prod = Product.objects.filter(pk=det.product_id.id).get()
    if det.product_id == prod:
      print(det.quantity)
      if prod.stock >= 0 or prod.stock >= det.quantity:
        new_stock = prod.stock - det.quantity
        print('El Stock luego de borrar es de: {}'.format(new_stock))
        prod.stock = new_stock
        prod.save()