from django.db import models
from usuario.models import User
from django.utils.translation import gettext as _
from base.models import BaseModel
# Create your models here.



class Employee(BaseModel):
  """Model definition for Empleado."""

  # TODO: Define fields here
  user_id = models.OneToOneField(User, on_delete=models.CASCADE)
  address = models.CharField(_('Address'), max_length=255, blank=True, null=True)
  birthday = models.DateField(_('Birthday'), blank=True, null=True)
  start_at_work = models.DateField(_('Start at Work'), blank=True, null=True)
  salary = models.DecimalField(_('Salary'), decimal_places=2, max_digits=10)

  class Meta:
    """Meta definition for Empleado."""

    verbose_name = 'Empleado'
    verbose_name_plural = 'Empleados'
    db_table = 'employee'

  def __str__(self):
    """Unicode representation of Empleado."""
    return self.user_id.get_full_name()


  # TODO: Define custom methods here
