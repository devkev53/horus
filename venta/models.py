from collections.abc import Iterable
from decimal import Decimal
from typing import Any
from django.db import models
from cliente.models import Client
from empleado.models import Employee
from base.models import BaseModel
from catalogo.models import Product
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.forms import model_to_dict


# Create your models here.


class Sale(BaseModel):
  """Model definition for Venta."""

  # TODO: Define fields here
  date = models.DateField()
  client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
  time = models.TimeField(auto_now_add=True)
  serie = models.CharField(max_length=255, blank=True, null=True)
  dte = models.CharField(max_length=255, blank=True, null=True)
  authorization_date = models.CharField(max_length=255, blank=True, null=True)
  total = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)

  class Meta:
    """Meta definition for Venta."""

    verbose_name = 'Venta'
    verbose_name_plural = 'Ventas'

  def __str__(self):
    """Unicode representation of Venta."""
    return '%s - %s -%s' % (self.created, self.client_id, self.total)

  def save(self, *args, **kwargs):
    if not self.pk is None:
      from catalogo.utils import activate_sale_edit_stock
      activate_sale_edit_stock(self)
    return super(Sale, self).save(*args, **kwargs)


  # TODO: Define custom methods here
  def toJSON(self):
    item = model_to_dict(self)
    item['client_id'] = self.client_id.toJSON()
    item['time'] = format(self.time, '%H:%M:%S')
    item['total'] = format(self.total, '.2f')
    item['det'] = [i.toJSON() for i in self.saledetail_set.all()]
    return item



class SaleDetail(models.Model):
  """Model definition for SaleDetail."""

  # TODO: Define fields here
  sale_id = models.ForeignKey(Sale, on_delete=models.CASCADE)
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveSmallIntegerField(default=1)
  total = models.DecimalField(max_digits=10, decimal_places=2)

  class Meta:
    """Meta definition for SaleDetail."""

    verbose_name = 'SaleDetail'
    verbose_name_plural = 'SaleDetails'

  def __str__(self):
    """Unicode representation of SaleDetail."""
    return '%s' % (self.total)

  # TODO: Define custom methods here

  def toJSON(self):
    item = model_to_dict(self, exclude=['sale_id'])
    item['product_id'] = self.product_id.toJSON()
    item['total'] = format(self.total, '.2f')
    return item

  def calculate_total(self):
    total = Decimal(self.product_id.price_sale) * Decimal(self.quantity)
    return "{:.2f}".format(Decimal(total))



# -*-*-*-*-*-*- PRE DELETE SIGNAL -*-*-*-*-*-*-
# @receiver(pre_delete, sender=SaleDetail)
# def delete_sale_detail_signal(sender, instance, **kwargs):
#     from catalogo.utils import delete_SaleDetail_edit_stock
#     delete_SaleDetail_edit_stock(instance)
#     print('se ha borrado un detalle')
#     # print(instance)