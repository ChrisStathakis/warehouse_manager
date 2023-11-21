from import_export import resources
from django.http import HttpResponse

from .models import PaymentMethod


class PaymentMethodResources(resources.ModelResource):

    class Meta:
        model = PaymentMethod


def backup_payment_methods_view(request):
    data = PaymentMethodResources().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="payment_methods.xls"'
    return response