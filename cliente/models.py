from django.db import models
from django.utils.translation import gettext as _
from base.models import BaseModel

# Create your models here.


class Client(BaseModel):
  """Model definition for Cliente."""

  # TODO: Define fields here
  name = models.CharField(_('Name'), max_length=100)
  last_name = models.CharField(_('Last Name'), max_length=100)
  address = models.CharField(_('Address'), max_length=255)
  nit = models.CharField(_('NIT'), max_length=25)
  phone = models.CharField(_('Phone'), max_length=15)

  class Meta:
    """Meta definition for Cliente."""

    verbose_name = 'Cliente'
    verbose_name_plural = 'Clientes'
    db_table = 'client'

  def __str__(self):
    """Unicode representation of Cliente."""
    return self.get_full_name()


  # TODO: Define custom methods here

  def get_full_name(self):
    if self.last_name:
      return '%s %s' % (self.name, self.last_name)
    else:
      return self.name
