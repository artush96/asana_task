from django.contrib import admin
from .models import *


class ASUserAdmin(admin.ModelAdmin):
    list_display_links = ['id']
    list_display = ['id', 'as_user_gid', 'name']
    list_editable = ['as_user_gid', 'name']


class TeamAdmin(admin.ModelAdmin):
    list_display_links = ['id']
    list_display = ['id', 'team_gid', 'title']
    list_editable = ['team_gid', 'title']


class ProjectAdmin(admin.ModelAdmin):
    list_display_links = ['id']
    list_display = ['id', 'project_gid', 'name']
    list_editable = ['project_gid', 'name']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class TaskAdmin(admin.ModelAdmin):
    list_display_links = ['id']
    list_display = ['id', 'task_gid', 'project', 'description', 'task_completion', 'performer']
    list_editable = ['task_gid', 'project', 'description', 'task_completion', 'performer']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class AccesTokenAdmin(admin.ModelAdmin):
    list_display_links = ['id']
    list_display = ['id', 'token', 'active_token']
    list_editable = ['token', 'active_token']


admin.site.register(AccesToken, AccesTokenAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Tasks, TaskAdmin)
admin.site.register(ASUser, ASUserAdmin)
admin.site.register(Team, TeamAdmin)
