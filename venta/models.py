from django.db import models
from cliente.models import Client
from empleado.models import Employee
from base.models import BaseModel
# Create your models here.


class Sale(models.Model):
  """Model definition for Venta."""

  # TODO: Define fields here

  class Meta:
    """Meta definition for Venta."""

    verbose_name = 'Venta'
    verbose_name_plural = 'Ventas'

  def __str__(self):
    """Unicode representation of Venta."""
    pass


  # TODO: Define custom methods here
