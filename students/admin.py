from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'telegram_username', 'email', 'student_type', 'teacher', 'get_organization', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone', 'telegram_username', 'email')
    list_filter = ('student_type', 'teacher__organization', 'created_at')
    ordering = ('-created_at',)
    
    def get_organization(self, obj):
        """Get organization through teacher"""
        if obj.teacher:
            return obj.teacher.organization.organization_name
        return '-'
    get_organization.short_description = 'Muassasa'
    get_organization.admin_order_field = 'teacher__organization'
    
    fieldsets = (
        ('Shaxsiy ma\'lumotlar', {
            'fields': ('first_name', 'last_name', 'phone', 'email', 'telegram_username')
        }),
        ('Tashkilot ma\'lumotlari', {
            'fields': ('student_type', 'teacher')
        }),
    )
