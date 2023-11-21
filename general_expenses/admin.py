from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import GeneralExpense, GeneralExpenseCategory
# Register your models here.


@admin.register(GeneralExpenseCategory)
class GenreralExpenseCateAdmin(ImportExportModelAdmin):
    pass


@admin.register(GeneralExpense)
class GenreralExpenseAdmin(ImportExportModelAdmin):
    pass

