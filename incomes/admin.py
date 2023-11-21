from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Income


@admin.register(Income)
class IncomeAdmin(ImportExportModelAdmin):
    pass