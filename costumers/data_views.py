from import_export import resources
from django.http import HttpResponse
from .models import Costumer, CostumerDetails, MyCard, InvoiceItem, PaymentInvoice


class CostumerResource(resources.ModelResource):

    class Meta:
        model = Costumer


class CostumerDetailsResource(resources.ModelResource):

    class Meta:
        model = CostumerDetails
        
        
class MyCardResource(resources.ModelResource):

    class Meta:
        model = MyCard
        
        
class InvoiceItemResource(resources.ModelResource):

    class Meta:
        model = InvoiceItem


class PaymentInvoiceResource(resources.ModelResource):
    class Meta:
        model = PaymentInvoice


def backup_customers_view(request):
    data = CostumerResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="customers.xls"'
    return response


def backup_customers_details_view(request):
    data = CostumerDetailsResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="customers_details.xls"'
    return response


def backup_my_card_view(request):
    data = MyCardResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="my_cards.xls"'
    return response


def backup_payments_invoices_view(request):
    data = PaymentInvoiceResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="payment_invoices.xls"'
    return response


def backup_invoice_items_view(request):
    data = InvoiceItemResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="invoice_items.xls"'
    return response