from django.contrib import admin
from .models import Goals, Analysis


class GoalsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class AnalysisAdmin(admin.ModelAdmin):
    list_display = ['id', 'goal']


# Register your models here.
admin.site.register(Goals, GoalsAdmin)
admin.site.register(Analysis, AnalysisAdmin)
