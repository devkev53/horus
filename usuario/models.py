from django.db import models
import uuid
from django.utils.translation import gettext as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from base.manager import UserManager
from django.utils.html import format_html

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):

  username = models.CharField(_('Username'), max_length=150, validators=[UnicodeUsernameValidator], unique=True)
  reset_token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)
  email = models.EmailField(_('Email'), max_length=150, unique=True, blank=False, null=False)
  name = models.CharField(_('Name'), max_length=150, blank=True, null=True)
  last_name = models.CharField(_('Last name'), max_length=150, blank=True, null=True)

  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserManager()

  class Meta:
    verbose_name = _('Usuario')
    verbose_name_plural = _('Usuarios')
    db_table = _("user")


  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email', 'name', 'last_name']

  def natural_key(self):
    return self.username

  def __str__(self):
    return f'{self.username}'

  def get_full_name(self):
    if self.last_name:
      return '%s %s' % (self.name, self.last_name)
    else:
      return self.name