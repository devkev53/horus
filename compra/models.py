from django.db import models
from base.models import BaseModel
from django.utils.translation import gettext as _
from proveedor.models import Providers
from catalogo.models import Product
from django.forms import model_to_dict
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, pre_save
from simple_history.models import HistoricalRecords


# Create your models here.




class Buy(BaseModel):
  """Model definition for Buy."""

  # TODO: Define fields here
  date = models.DateField(_('Date'))
  serie = models.CharField(_('Serie'), max_length=255, blank=True, null=True)
  reference = models.CharField(_('Reference'), max_length=255, blank=True, null=True)
  provider_id = models.ForeignKey(Providers, on_delete=models.CASCADE)
  is_paid = models.BooleanField(_('Is Paid'), default=False)
  document = models.FileField(_('Document'), upload_to='buy/document/', blank=True, null=True)
  total = models.DecimalField(_('Total'), decimal_places=2, max_digits=10, default=0.00)
  history = HistoricalRecords()

  class Meta:
    """Meta definition for Buy."""

    verbose_name = 'Compra'
    verbose_name_plural = 'Compras'

  def __str__(self):
    """Unicode representation of Buy."""
    return '%s - %s - Q. %s' % (self.date, self.provider_id, self.total)

  def check_payment(self):
    total = 0
    for pay in Payment.objects.filter(is_active=True, buy_id=self.id):
      total += pay.total
    return total


  # TODO: Define custom methods here
  def toJSON(self):
    item = model_to_dict(self, exclude=['document'])
    item['provider_id'] = self.provider_id.toJSON()
    item['det'] = [i.toJSON() for i in self.buydetail_set.all()]
    item['chek_payment'] = self.check_payment()
    return item



class BuyDetail(BaseModel):
  """Model definition for BuyDetail."""

  # TODO: Define fields here
  buy_id = models.ForeignKey(Buy, on_delete=models.CASCADE)
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveSmallIntegerField(_('Quantity'), default=1)
  sub_total = models.DecimalField(_('Subtotal'), max_digits=10, decimal_places=2)

  class Meta:
    """Meta definition for BuyDetail."""

    verbose_name = 'Detalle de compra'
    verbose_name_plural = 'Detalle de compras'

  def __str__(self):
    """Unicode representation of BuyDetail."""
    return '%s: %s - %s -%s' % (self.buy_id.provider_id, self.product_id.name, self.quantity, self.sub_total)

  # TODO: Define custom methods here

  def toJSON(self):
    item = model_to_dict(self, exclude=['buy_id'])
    item['product_id'] = self.product_id.toJSON()
    item['sub_total'] = format(self.sub_total, '.2f')
    return item



class Payment(BaseModel):
  """Model definition for Payment."""

  # TODO: Define fields here
  buy_id = models.ForeignKey(Buy, on_delete=models.CASCADE)
  reference = models.CharField(_('Reference'), max_length=255, blank=True, null=True)
  payment_type = models.CharField(_('Payment Type'),max_length=255)
  document = models.FileField(_('Document'), upload_to='payment/document/', blank=True, null=True)
  total = models.DecimalField(_('Total'), max_digits=10, decimal_places=2)

  class Meta:
    """Meta definition for Payment."""

    verbose_name = 'Pago'
    verbose_name_plural = 'Pagos'

  def __str__(self):
    """Unicode representation of Payment."""
    return '%s - %s - %s' % (self.buy_id, self.payment_type, self.total)


  # TODO: Define custom methods here

  def toJSON(self):
    item = model_to_dict(self, exclude=['document'])
    item['buy_id'] = self.buy_id.toJSON()
    item['date'] = self.created
    item['document'] = self.get_document_url()
    item['total'] = format(self.total, '.2f')
    return item

  def get_document_url(self):
    if self.document:
      return True
    else:
      return False




# -*-*-*-*-*-*- POST DELETE SIGNAL -*-*-*-*-*-*-
@receiver(post_delete, sender=BuyDetail)
def delete_buy_detail_signal(sender, instance, *args, **kwargs):
    from catalogo.utils import update_product_stock
    update_product_stock()
    # print(instance)


# -*-*-*-*-*-*- POST SAVE SIGNAL -*-*-*-*-*-*-
@receiver(post_save, sender=Payment)
def update_buy_state(sender, instance, *args, **kwargs):
  total_payment = 0
  print(instance.buy_id.id)
  buy = Buy.objects.filter(pk=instance.buy_id.pk).get()
  for pays in Payment.objects.filter(buy_id=instance.buy_id):
    total_payment += pays.total
  if total_payment >= buy.total:
    buy.is_paid = True
    buy.save()