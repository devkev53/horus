from django.db import models
from django.utils.translation import gettext as _
from base.models import BaseModel
from django.forms import model_to_dict
from app.settings.local import DOMAIN


# Create your models here.


class Providers(BaseModel):
  """Model definition for Proveedor."""

  # TODO: Define fields here
  logo = models.ImageField(_('Company Logo'), upload_to='company/logos/', blank=True, null=True)
  company_name = models.CharField(_('Company Name'), max_length=125)
  reference_contact = models.CharField(_('Reference Contact'), max_length=125)
  address = models.CharField(_('Address'), max_length=255, blank=True, null=True)
  phone = models.CharField(_('Phone'), max_length=15, blank=True, null=True)
  nit = models.CharField(_('NIT'), max_length=15)

  class Meta:
    """Meta definition for Proveedor."""

    verbose_name = 'Proveedor'
    verbose_name_plural = 'Proveedores'
    db_table = 'Providers'

  def __str__(self):
    """Unicode representation of Proveedor."""
    return '{}-{}-{}'.format(
      self.company_name, self.reference_contact, self.phone
    )

  # TODO: Define custom methods here

  def toJSON(self):
    item = model_to_dict(self)
    item['logo'] = self.get_url_img()
    return item

  def get_url_img(self):
    if self.logo:
      return '{}{}'.format(DOMAIN, self.logo.url)
    else:
      return ''

