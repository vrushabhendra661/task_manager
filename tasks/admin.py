from django.contrib import admin
from .models import Task, TaskActivity

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'priority', 'location', 'created_at', 'due_date']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['created_at', 'updated_at', 'weather_info']

@admin.register(TaskActivity)
class TaskActivityAdmin(admin.ModelAdmin):
    list_display = ['task', 'action', 'timestamp']
    list_filter = ['action', 'timestamp']
    readonly_fields = ['timestamp']