from django.contrib import admin  # preimported by django
from .models import Goals, Analysis #manually imported by me


class GoalsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user']
    search_fields = ['name']


class AnalysisAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'goal']
    search_fields = ['goal']


# Register your models here.
admin.site.register(Goals, GoalsAdmin)
admin.site.register(Analysis, AnalysisAdmin)
