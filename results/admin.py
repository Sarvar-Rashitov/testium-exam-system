from django.contrib import admin
from .models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'score', 'percentage', 'band_score', 'time_taken', 'completed_at')
    list_filter = ('exam', 'completed_at')
    search_fields = ('student__first_name', 'student__last_name', 'exam__title')
    readonly_fields = ('score', 'percentage', 'band_score', 'completed_at')
    ordering = ('-completed_at',)
    
    def band_score(self, obj):
        return obj.band_score
    band_score.short_description = 'Band Score'
