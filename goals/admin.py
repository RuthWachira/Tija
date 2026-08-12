from django.contrib import admin  # preimported by django
from .models import Goal  # manually imported by me


class GoalAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user']
    search_fields = ['name']
    readonly_fields = ['created_at']


# Register your models here.
admin.site.register(Goal, GoalAdmin)
