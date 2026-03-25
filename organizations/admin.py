from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Organization


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
