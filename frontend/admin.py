from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from  frontend.models import PaymentMethod, PAYMENT_METHOD_CATEGORY


@admin.register(PaymentMethod)
class PaymentMethodAdmin(ImportExportModelAdmin):
    pass



