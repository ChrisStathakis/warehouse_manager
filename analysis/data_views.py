from import_export import resources
from django.http import HttpResponse
from .models import TaxesModifier


class TaxesModifierResource(resources.ModelResource):

    class Meta:
        model = TaxesModifier


def backup_taxes_view(request):
    data = TaxesModifierResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="taxes_modifiers.xls"'
    return response

