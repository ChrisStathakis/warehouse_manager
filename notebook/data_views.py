from import_export.resources import ModelResource
from django.http import HttpResponse

from .models import NoteBook, Tags


class NoteBookResources(ModelResource):
    class Meta:
        model = NoteBook


class TagsResources(ModelResource):
    class Meta:
        model = NoteBook

def backup_notebook_view(request):
    data = NoteBookResources().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="notebook.xls"'
    return response


def backup_tags_view(request):
    data = NoteBookResources().export().xls
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="tags.xls"'
    return response

