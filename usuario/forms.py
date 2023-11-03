from django import forms
from usuario.models import User
from django.contrib.auth import get_user_model

class UserForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'w-full bg-gray-50 border border-zinc-300 text-zinc-600 focus:outline-none focus:border-zinc-500 p-1.5 px-2 rounded-lg'
      form.field.widget.attrs['autocomplete'] = 'off'

  class Meta:
    model = User
    fields = (
      'username', 'email', 'name', 'last_name', 'password'
    )

class UserUpdateForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'w-full bg-gray-50 border border-zinc-300 text-zinc-600 focus:outline-none focus:border-zinc-500 p-1.5 px-2 rounded-lg'
      form.field.widget.attrs['autocomplete'] = 'off'

  class Meta:
    model = User
    fields = (
      'name', 'last_name'
    )