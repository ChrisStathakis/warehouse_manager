from import_export import resources
from django.http import HttpResponse
from .models import Vendor, VendorBankingAccount, Invoice, Payment, Employer, Note


class VendorResource(resources.ModelResource):

    class Meta:
        model = Vendor


class VendorBankingAccountResource(resources.ModelResource):

    class Meta:
        model = VendorBankingAccount


class InvoiceResource(resources.ModelResource):

    class Meta:
        model = Invoice


class PaymentResource(resources.ModelResource):

    class Meta:
        model = Payment


class EmployerResource(resources.ModelResource):

    class Meta:
        model = Employer


class NoteResource(resources.ModelResource):

    class Meta:
        model = Note


def backup_invoices_view(request):
    data = InvoiceResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="invoices.xls"'
    return response


def backup_vendors_view(request):
    data = VendorResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="vendors.xls"'
    return response


def backup_vendor_payments_view(request):
    data = PaymentResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="vendor_payments.xls"'
    return response


def backup_vendor_notes_view(request):
    data = NoteResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="vendor_notes.xls"'
    return response


def backup_vendor_employers_view(request):
    data = EmployerResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="vendor_employers.xls"'
    return response


def backup_vendor_banking_account_view(request):
    data = VendorBankingAccountResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="vendor_banking_account.xls"'
    return response

