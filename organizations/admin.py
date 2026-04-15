from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Organization, Teacher, OrganizationSettings, Group


@admin.register(Organization)
class OrganizationAdmin(UserAdmin):
    list_display = ('username', 'organization_name', 'email', 'phone', 'created_at')
    list_filter = ('is_staff', 'is_active', 'created_at')
    search_fields = ('username', 'organization_name', 'email')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Organization Info', {'fields': ('organization_name', 'phone')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Organization Info', {'fields': ('organization_name', 'phone', 'email')}),
    )


@admin.register(OrganizationSettings)
class OrganizationSettingsAdmin(admin.ModelAdmin):
    list_display = ['organization', 'allow_student_registration', 'updated_at']
    search_fields = ['organization__organization_name']
    fieldsets = (
        ('Tashkilot', {
            'fields': ('organization',)
        }),
        ('Brending', {
            'fields': ('logo',)
        }),
        ('Xabarnomalar', {
            'fields': ('email_notifications', 'telegram_notifications', 'telegram_bot_token')
        }),
        ('Platforma sozlamalari', {
            'fields': ('allow_student_registration', 'show_leaderboard', 'enable_certificates')
        }),
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'organization', 'subject', 'phone', 'is_active', 'created_at')
    list_filter = ('is_active', 'organization', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone', 'email', 'subject')
    ordering = ('organization', 'first_name', 'last_name')
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('organization', 'first_name', 'last_name', 'subject')
        }),
        ('Aloqa ma\'lumotlari', {
            'fields': ('phone', 'email')
        }),
        ('Holat', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'organization', 'lesson_time', 'student_count', 'is_ongoing', 'is_active', 'created_at')
    list_filter = ('is_active', 'organization', 'teacher', 'created_at')
    search_fields = ('name', 'teacher__first_name', 'teacher__last_name', 'description')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('organization', 'teacher', 'name', 'description')
        }),
        ('Jadval', {
            'fields': ('weekdays', 'lesson_time')
        }),
        ('Sanalar', {
            'fields': ('start_date', 'end_date')
        }),
        ('Holat', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def student_count(self, obj):
        return obj.student_count
    student_count.short_description = "O'quvchilar soni"

