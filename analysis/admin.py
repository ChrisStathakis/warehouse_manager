from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import TaxesModifier
# Register your models here.


@admin.register(TaxesModifier)
class TaxesModifier(ImportExportModelAdmin):
    pass