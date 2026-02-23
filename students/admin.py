from django.contrib import admin
from .models import Students


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    """Admin interface for managing Students"""
    list_display = ['s_id', 's_name', 's_dept', 'created_at', 'updated_at']
    list_filter = ['s_dept', 'created_at']
    search_fields = ['s_id', 's_name', 's_dept']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
