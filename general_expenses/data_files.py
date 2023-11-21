from import_export import resources
from django.http import HttpResponse

from .models import GeneralExpense, GeneralExpenseCategory


class GeneralExpenseResources(resources.ModelResource):
    class Meta:
        model = GeneralExpense


class GeneralExpenseCategoryResources(resources.ModelResource):
    class Meta:
        model = GeneralExpense

def backup_general_expenses_folder_view(request):
    data = GeneralExpenseResources().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="general_expenses_folder.xls"'
    return response



def backup_general_expenses_category_folder_view(request):
    data = GeneralExpenseCategoryResources().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="general_expenses_category_folder.xls"'
    return response