from django.db import models
from django.utils.translation import gettext as _
from base.models import BaseModel

# Create your models here.


class Supplier(BaseModel):
  """Model definition for Proveedor."""

  # TODO: Define fields here
  company_name = models.CharField(_('Company Name'), max_length=125)
  reference_contact = models.CharField(_('Reference Contact'), max_length=125)
  address = models.CharField(_('Address'), max_length=255)
  phone = models.CharField(_('Phone'), max_length=15)

  class Meta:
    """Meta definition for Proveedor."""

    verbose_name = 'Proveedor'
    verbose_name_plural = 'Proveedores'
    db_table = 'supplier'

  def __str__(self):
    """Unicode representation of Proveedor."""
    return '{}-{}-{}'.format(
      self.company_name, self.reference_contact, self.phone
    )


  # TODO: Define custom methods here
