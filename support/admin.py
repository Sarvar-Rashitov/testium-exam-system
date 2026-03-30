from django.contrib import admin
from .models import SupportVideo, FAQ, ContactInfo, SupportTicket, TeamMember


@admin.register(SupportVideo)
class SupportVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'duration', 'order', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order', '-created_at']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_active']
    ordering = ['order', '-created_at']


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'email', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['title', 'email', 'phone']


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['organization', 'subject', 'category', 'status', 'priority', 'created_at']
    list_filter = ['status', 'priority', 'category', 'created_at']
    search_fields = ['subject', 'message', 'organization__organization_name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('organization', 'subject', 'message', 'category', 'attachment')
        }),
        ('Holat', {
            'fields': ('status', 'priority', 'admin_response', 'resolved_at')
        }),
        ('Vaqt', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'position', 'bio']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'name']
