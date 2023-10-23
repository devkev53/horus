from django.db import models
from django.utils.translation import gettext as _
from base.models import BaseModel
from django.forms import model_to_dict

# Create your models here.


class Client(BaseModel):
  """Model definition for Cliente."""

  # TODO: Define fields here
  name = models.CharField(_('Name'), max_length=100)
  last_name = models.CharField(_('Last Name'), max_length=100, blank=True, null=True)
  address = models.CharField(_('Address'), max_length=255, blank=True, null=True)
  nit = models.CharField(_('NIT'), max_length=25, default='C/F', blank=True, null=True)
  phone = models.CharField(_('Phone'), max_length=15, blank=True, null=True)

  class Meta:
    """Meta definition for Cliente."""

    verbose_name = 'Cliente'
    verbose_name_plural = 'Clientes'
    db_table = 'client'

  def __str__(self):
    """Unicode representation of Cliente."""
    return self.get_full_name()


  # TODO: Define custom methods here

  def toJSON(self):
    item = model_to_dict(self)
    item['get_full_name'] = self.get_full_name()
    return item

  def get_full_name(self):
    if self.last_name:
      return '%s %s' % (self.name, self.last_name)
    else:
      return self.name
