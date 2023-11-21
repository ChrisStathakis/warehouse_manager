from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Payroll, BillCategory, Bill, Occupation, Person, GenericExpense, GenericExpenseCategory
# Register your models here.


@admin.register(Payroll)
class PayrollAdmin(ImportExportModelAdmin):
    pass

@admin.register(BillCategory)
class BillCategoryAdmin(ImportExportModelAdmin):
    pass


@admin.register(Bill)
class BillAdmin(ImportExportModelAdmin):
    pass



@admin.register(Occupation)
class OccupationAdmin(ImportExportModelAdmin):
    pass



@admin.register(Person)
class PersonAdmin(ImportExportModelAdmin):
    pass



@admin.register(GenericExpense)
class GenericExpenseAdmin(ImportExportModelAdmin):
    pass


@admin.register(GenericExpenseCategory)
class GenericExpenseCategoryAdmin(ImportExportModelAdmin):
    pass
