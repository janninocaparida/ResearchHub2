from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponse
import csv
from datetime import datetime
from .models import Students


class StudentDepartmentFilter(admin.SimpleListFilter):
    """Custom filter for department with counts"""
    title = 'Department'
    parameter_name = 'department'
    
    def lookups(self, request, model_admin):
        departments = Students.objects.values_list('s_dept', flat=True).distinct()
        return [(dept, dept) for dept in departments]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(s_dept=self.value())
        return queryset


class DateRangeFilter(admin.SimpleListFilter):
    """Custom filter for creation date ranges"""
    title = 'Created Date Range'
    parameter_name = 'date_range'
    
    def lookups(self, request, model_admin):
        return (
            ('today', 'Today'),
            ('this_week', 'This Week'),
            ('this_month', 'This Month'),
            ('this_year', 'This Year'),
        )
    
    def queryset(self, request, queryset):
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        
        if self.value() == 'today':
            return queryset.filter(created_at__date=now.date())
        elif self.value() == 'this_week':
            week_start = now - timedelta(days=now.weekday())
            return queryset.filter(created_at__gte=week_start)
        elif self.value() == 'this_month':
            return queryset.filter(created_at__year=now.year, created_at__month=now.month)
        elif self.value() == 'this_year':
            return queryset.filter(created_at__year=now.year)
        return queryset


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    """Advanced admin interface for managing Students with custom actions and filtering"""
    
    # Display configuration
    list_display = ['student_id_display', 'student_name_display', 'department_display', 
                    'created_date_display', 'updated_date_display', 'record_status']
    
    # Filtering options
    list_filter = [StudentDepartmentFilter, DateRangeFilter, 'created_at', 'updated_at']
    
    # Search fields
    search_fields = ['s_id', 's_name', 's_dept']
    
    # Read-only fields
    readonly_fields = ['created_at', 'updated_at', 'record_info']
    
    # Field grouping and organization
    fieldsets = (
        ('Student Information', {
            'fields': ('s_id', 's_name', 's_dept'),
            'description': 'Basic student details'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'record_info'),
            'classes': ('collapse',),
            'description': 'Record creation and modification times'
        }),
    )
    
    # Ordering
    ordering = ['-created_at']
    
    # Pagination
    list_per_page = 25
    
    # Custom actions
    actions = [
        'export_as_csv',
        'export_as_json',
        'mark_as_reviewed',
        'generate_report',
        'bulk_update_department',
    ]
    
    # Enable date hierarchy
    date_hierarchy = 'created_at'
    
    # Autocomplete styling
    list_display_links = ['student_name_display']
    
    # Custom methods for display
    def student_id_display(self, obj):
        """Display student ID with custom styling"""
        return format_html(
            '<span style="background-color: #e3f2fd; padding: 5px 10px; border-radius: 5px; font-weight: bold;">{}</span>',
            obj.s_id
        )
    student_id_display.short_description = 'Student ID'
    
    def student_name_display(self, obj):
        """Display student name with link to edit"""
        return format_html(
            '<a href="/admin/students/students/{}/change/">{}</a>',
            obj.id,
            obj.s_name
        )
    student_name_display.short_description = 'Student Name'
    
    def department_display(self, obj):
        """Display department with colored badge"""
        colors = {
            'Computer Science': '#4CAF50',
            'Engineering': '#2196F3',
            'Business': '#FF9800',
            'Arts': '#9C27B0',
        }
        color = colors.get(obj.s_dept, '#757575')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 5px; display: inline-block;">{}</span>',
            color,
            obj.s_dept
        )
    department_display.short_description = 'Department'
    
    def created_date_display(self, obj):
        """Display creation date in readable format"""
        return obj.created_at.strftime('%b %d, %Y %H:%M') if obj.created_at else 'N/A'
    created_date_display.short_description = 'Created'
    
    def updated_date_display(self, obj):
        """Display update date in readable format"""
        return obj.updated_at.strftime('%b %d, %Y %H:%M') if obj.updated_at else 'N/A'
    updated_date_display.short_description = 'Updated'
    
    def record_status(self, obj):
        """Display record status indicator"""
        from datetime import timedelta
        from django.utils import timezone
        
        if obj.updated_at and obj.created_at:
            time_diff = obj.updated_at - obj.created_at
            if time_diff.total_seconds() > 60:  # Modified
                return format_html(
                    '<span style="color: #FF6F00; font-weight: bold;">⚡ Modified</span>'
                )
        
        return format_html(
            '<span style="color: #4CAF50; font-weight: bold;">✓ Active</span>'
        )
    record_status.short_description = 'Status'
    
    def record_info(self, obj):
        """Display detailed record information"""
        if obj.created_at:
            created = obj.created_at.strftime('%B %d, %Y at %H:%M:%S')
            updated = obj.updated_at.strftime('%B %d, %Y at %H:%M:%S') if obj.updated_at else 'Never'
            return format_html(
                '<div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px;">'
                '<p><strong>Created:</strong> {}</p>'
                '<p><strong>Last Updated:</strong> {}</p>'
                '</div>',
                created,
                updated
            )
        return 'No timestamp information'
    record_info.short_description = 'Record Information'
    
    # Custom Admin Actions
    def export_as_csv(self, request, queryset):
        """Export selected records as CSV file"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="students_{}.csv"'.format(
            datetime.now().strftime('%Y%m%d_%H%M%S')
        )
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Student ID', 'Name', 'Department', 'Created', 'Updated'])
        
        for student in queryset:
            writer.writerow([
                student.id,
                student.s_id,
                student.s_name,
                student.s_dept,
                student.created_at.strftime('%Y-%m-%d %H:%M:%S') if student.created_at else '',
                student.updated_at.strftime('%Y-%m-%d %H:%M:%S') if student.updated_at else '',
            ])
        
        return response
    export_as_csv.short_description = '📥 Export Selected as CSV'
    
    def export_as_json(self, request, queryset):
        """Export selected records as JSON file"""
        import json
        
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="students_{}.json"'.format(
            datetime.now().strftime('%Y%m%d_%H%M%S')
        )
        
        data = []
        for student in queryset:
            data.append({
                'id': student.id,
                's_id': student.s_id,
                's_name': student.s_name,
                's_dept': student.s_dept,
                'created_at': student.created_at.isoformat() if student.created_at else None,
                'updated_at': student.updated_at.isoformat() if student.updated_at else None,
            })
        
        json.dump(data, response, indent=2, default=str)
        return response
    export_as_json.short_description = '📤 Export Selected as JSON'
    
    def mark_as_reviewed(self, request, queryset):
        """Mark records as reviewed by updating timestamp"""
        from django.utils import timezone
        updated_count = queryset.update(updated_at=timezone.now())
        self.message_user(request, f'✓ Successfully marked {updated_count} record(s) as reviewed.')
    mark_as_reviewed.short_description = '✅ Mark Selected as Reviewed'
    
    def generate_report(self, request, queryset):
        """Generate summary report for selected records"""
        total = queryset.count()
        departments = queryset.values('s_dept').distinct().count()
        message = f'📊 Report: {total} student(s) from {departments} department(s)'
        self.message_user(request, message)
    generate_report.short_description = '📊 Generate Summary Report'
    
    def bulk_update_department(self, request, queryset):
        """Placeholder for bulk department update"""
        self.message_user(request, f'💼 Ready to update {queryset.count()} record(s). (Feature available in next version)')
    bulk_update_department.short_description = '💼 Bulk Update Department'
    
    # Make admin changelist impressive
    class Media:
        css = {
            'all': ('admin/css/admin.css',)
        }
