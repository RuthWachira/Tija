from django.contrib import admin  # preimported by django
# manually imported by me
from .models import Goal, Challenge, Win, ChallengeRemediation


class GoalAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user']
    search_fields = ['name']
    readonly_fields = ['created_at']


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['id', 'goal', 'title', 'remediability']
    search_fields = ['title']
    readonly_fields = ['created_at']


class WinAdmin(admin.ModelAdmin):
    list_display = ['id', 'goal', 'title']
    search_fields = ['title']
    readonly_fields = ['created_at']


class ChallengeRemediationAdmin(admin.ModelAdmin):
    list_display = ['id', 'challenge', 'title']
    search_fields = ['title']
    readonly_fields = ['created_at']


# Register your models here.
admin.site.register(Goal, GoalAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Win, WinAdmin)
admin.site.register(ChallengeRemediation, ChallengeRemediationAdmin)
