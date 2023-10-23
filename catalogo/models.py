from django.db import models
from django.utils.translation import gettext as _
from django.utils.html import format_html
from base.models import BaseModel

# Create your models here.

class Category(BaseModel):
  """Model definition for Categoria."""

  # TODO: Define fields here
  name = models.CharField(_('Name'), max_length=255)
  image = models.ImageField(upload_to='categories/image', blank=True, null=True)


  class Meta:
    """Meta definition for Categoria."""

    verbose_name = 'Categoria'
    verbose_name_plural = 'Categorias'
    db_table = 'category'

  def __str__(self):
    """Unicode representation of Categoria."""
    return self.name

  # TODO: Define custom methods here

  def get_url_img(self):
    if self.image:
      return 'http://localhost:8000{}'.format(self.image.url)
    else:
      return ''


class Product(BaseModel):
  """Model definition for Producto."""

  # TODO: Define fields here
  name = models.CharField(_('Name'), max_length=255)
  description = models.TextField(_('Description'), blank=True, null=True)
  image = models.ImageField(_('Image'), upload_to='product/', blank=True, null=True)
  category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

  class Meta:
    """Meta definition for Producto."""

    verbose_name = 'Producto'
    verbose_name_plural = 'Productos'
    db_table = 'product'

  def __str__(self):
    """Unicode representation of Producto."""
    return "{} - {}".format(self.name, self.sale_price)

  # TODO: Define custom methods here

  def preview_img(self):
    if not self.image:
      data = 'https://www.cjoint.com/doc/20_12/JLFrj6Sanqu_image-not-found.png'
    else:
      data = self.image.url
      # print(data)

    return format_html(
      '<picture style="width:30px; height:30px; border:2px solid #FFF; overflow:hidden; justify-content:center; display:flex; border-radius: 100%;"><img src="{}" style="object-fit:cover; height:100%;;"/></picture>',
      data,
    )
  preview_img.short_description = _('Image')