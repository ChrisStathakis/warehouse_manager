from django.contrib import admin
from .models import Costumer, PaymentInvoice, InvoiceItem, MyCard, CostumerDetails, PaymentMethod

from import_export.admin import ImportExportModelAdmin


def make_published(modeladmin, request, queryset):
    for ele in queryset:
        ele.save()
make_published.short_description = "Mark selected stories as published"


@admin.register(Costumer)
class CostumerAdmin(ImportExportModelAdmin):
    list_filter = ['active']
    search_fields = ['amka', 'first_name', 'last_name', 'cellphone', 'phone']
    list_display = ['eponimia', 'amka', 'balance', 'active']
    # readonly_fields = ['full_name']
    actions = [make_published, ]
    fieldsets = (
        ('Personal Info', {
            'fields': ('active', ('first_name', 'last_name'), 'amka', )
        }),
        ('Phones', {
            'fields': (('cellphone', 'phone'),)
        }),
        ('values', {
            'fields': (('paid_value', 'value'), 'balance'),
        }),
    )


@admin.register(PaymentInvoice)
class PaymentInvoiceAdmin(ImportExportModelAdmin):
    pass


@admin.register(CostumerDetails)
class CostumerDetailAdmin(ImportExportModelAdmin):
    list_display = ['costumer', 'afm']


@admin.register(InvoiceItem)
class PaymentItemAdmin(ImportExportModelAdmin):
    pass


@admin.register(MyCard)
class MyCardAdmin(ImportExportModelAdmin):
    list_display = ['title', 'favorite']


