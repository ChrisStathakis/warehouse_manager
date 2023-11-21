from import_export import resources
from django.http import HttpResponse

from .models import (Bill, BillCategory, Occupation, Person, Payroll, GenericExpenseCategory,
                     GenericExpense

                    )


class BillResource(resources.ModelResource):

    class Meta:
        model = Bill


class BillCategoryResource(resources.ModelResource):

    class Meta:
        model = BillCategory


class OccupationResource(resources.ModelResource):

    class Meta:
        model = Occupation


class PersonResource(resources.ModelResource):

    class Meta:
        model = Person


class PayrollResource(resources.ModelResource):

    class Meta:
        model = Payroll


class GenericExpenseCategoryResource(resources.ModelResource):

    class Meta:
        model = GenericExpenseCategory


class GenericExpenseResource(resources.ModelResource):

    class Meta:
        model = GenericExpense


def backup_bill_view(request):
    data = BillResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="bills.xls"'
    return response


def backup_bill_categories_view(request):
    data = BillCategoryResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="bill_categories.xls"'
    return response


def backup_occupation_view(request):
    data = OccupationResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="occupation.xls"'
    return response


def backup_persons_view(request):
    data = PersonResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response


def backup_payrolls_view(request):
    data = PayrollResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="payrolls.xls"'
    return response


def backup_generic_expenses_view(request):
    data = GenericExpenseResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="generic_expenses.xls"'
    return response


def backup_generic_expenses_category_view(request):
    data = GenericExpenseCategoryResource().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="generic_expenses_category.xls"'
    return response