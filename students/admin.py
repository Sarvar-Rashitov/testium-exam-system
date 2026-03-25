from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'telegram_username', 'email', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone', 'telegram_username', 'email')
    ordering = ('-created_at',)
