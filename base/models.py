from django.db import models
from usuario.models import User
from datetime import date
from crum import get_current_user
from django.utils.translation import gettext as _
from simple_history.models import HistoricalRecords

# Create your models here.

class BaseModel(models.Model):
  """Model definition for ModeloBase."""

  # TODO: Define fields here
  created_by = models.ForeignKey(
    User, verbose_name=_('Created by'),
    on_delete=models.PROTECT, related_name='created_by%(app_label)s_%(class)s_related',
    blank=True, null=True, editable=False
  )
  created = models.DateField(
    _('Created'), auto_now_add=True,
    blank=True, null=True
  )
  updated_by = models.ForeignKey(
    User, verbose_name=_('Updated by'),
    on_delete=models.PROTECT, related_name='updated_by%(app_label)s_%(class)s_related',
    blank=True, null=True, editable=False
  )
  updated = models.DateField(
    _('Updated'), auto_now=True,
    blank=True, null=True
  )
  is_active = models.BooleanField(_('Is Active'), default=True)
  history = HistoricalRecords()


  class Meta:
    """Meta definition for ModeloBase."""

    abstract = True
    verbose_name = 'ModeloBase'
    verbose_name_plural = 'ModeloBases'

  def __str__(self):
    """Unicode representation of ModeloBase."""
    pass

  def save(self, *args, **kwargs):
    """Save method for BaseModel."""
    # Guardando el user
    user = get_current_user()
    if user is not None:
        if not self.pk:
            self.created_by = user
        else:
            self.userUpdate = user
    super(BaseModel, self).save()

  # TODO: Define custom methods here

