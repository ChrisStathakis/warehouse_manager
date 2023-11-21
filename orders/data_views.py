from import_export import resources
from django.http import HttpResponse

from .models import Order, Payment


class OrderResource(resources.ModelResource):

    class Meta:
        model = Order


class PaymentResource(resources.ModelResource):

    class Meta:
        model = Payment


def backup_orders_view(request):
    data = OrderResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="orders.xls"'
    return response


def backup_orders_payment_view(request):
    data = PaymentResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="orders_payment.xls"'
    return response

