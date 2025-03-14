from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'created_at', 'due_date', 'city')
    list_filter = ('completed',)
    search_fields = ('title',)