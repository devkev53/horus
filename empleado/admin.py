from django.contrib import admin
from empleado.models import Employee

# Register your models here.

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
  '''Admin View for Employee'''

  list_display = ('id', 'user_id', 'birthday', 'start_at_work', 'salary')
  # list_filter = ('',)
  # inlines = [
  #   Inline,
  # ]
  # raw_id_fields = ('',)
  # readonly_fields = ('',)
  # search_fields = ('',)
  # date_hierarchy = ''
  # ordering = ('',)