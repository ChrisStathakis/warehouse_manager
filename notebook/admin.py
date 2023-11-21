from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Tags, NoteBook


@admin.register(Tags)
class TagAdmin(ImportExportModelAdmin):
    pass



@admin.register(NoteBook)
class NoteBookAdmin(ImportExportModelAdmin):
    pass