from import_export.resources import ModelResource
from django.http import HttpResponse

from .models import Income


class IncomeResources(ModelResource):
    class Meta:
        model = Income



def backup_incomes_view(request):
    data = IncomeResources().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="incomes.xls"'
    return response



