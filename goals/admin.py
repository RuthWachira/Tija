from django.contrib import admin  # preimported by django
from .models import Goal, Review  # manually imported by me


class GoalAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user']
    search_fields = ['name']
    readonly_fields = ['date_created']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'goal']
    search_fields = ['goal']
    readonly_fields = ['date_created']


# Register your models here.
admin.site.register(Goal, GoalAdmin)
admin.site.register(Review, ReviewAdmin)
