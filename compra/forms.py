from datetime import datetime
from django import forms
from compra.models import Buy, BuyDetail, Payment


class BuyForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'w-full bg-gray-50 border border-zinc-300 text-zinc-600 focus:outline-none focus:border-zinc-500 p-1.5 px-2 rounded-lg'
      form.field.widget.attrs['autocomplete'] = 'off'

  class Meta:
    model = Buy
    fields=(
      'date', 'serie', 'reference',
      'provider_id', 'is_paid', 'total',
      )
    widgets = {
      'date': forms.DateInput(
        format='%Y-%m-%d',
        attrs={
          'value': datetime.now().strftime('%Y-%m-%d')
        }
      ),
      'total': forms.NumberInput(
        attrs={
          'readonly':True
        }
      ),
    }