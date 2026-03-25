from django.contrib import admin
from .models import (
    Exam, Section, QuestionGroup, ExamLink,
    MultipleChoiceSingleQuestion, MultipleChoiceMultipleQuestion,
    TrueFalseNotGivenQuestion, YesNoNotGivenQuestion,
    SentenceCompletionQuestion, ShortAnswerQuestion,
    DiagramLabelingQuestion, SummaryCompletionQuestion,
    NoteCompletionQuestion, TableCompletionQuestion,
    FlowchartCompletionQuestion, MatchingHeadingsQuestion,
    MatchingInformationQuestion, MatchingFeaturesQuestion,
    MatchingSentenceEndingsQuestion, HeadingOption,
    FeatureOption, SentenceEndingOption
)


class SectionInline(admin.TabularInline):
    model = Section
    extra = 0
    fields = ('title', 'module', 'order', 'is_active')


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'duration', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'organization')
    search_fields = ('title', 'description')
    inlines = [SectionInline]
    ordering = ('-created_at',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'exam', 'module', 'order', 'is_active', 'created_at')
    list_filter = ('module', 'is_active', 'created_at')
    search_fields = ('title', 'exam__title')
    ordering = ('exam', 'order')


@admin.register(QuestionGroup)
class QuestionGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'question_type', 'order')
    list_filter = ('question_type', 'section__module')
    search_fields = ('title', 'instructions')
    ordering = ('section', 'order')


@admin.register(MultipleChoiceSingleQuestion)
class MultipleChoiceSingleAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'question_group', 'correct_answer', 'points')
    list_filter = ('question_group__section__exam',)
    search_fields = ('question_text',)
    ordering = ('question_group', 'question_number')


@admin.register(MultipleChoiceMultipleQuestion)
class MultipleChoiceMultipleAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'question_group', 'correct_answers', 'points')
    list_filter = ('question_group__section__exam',)
    search_fields = ('question_text',)
    ordering = ('question_group', 'question_number')


@admin.register(TrueFalseNotGivenQuestion)
class TrueFalseNotGivenAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'question_group', 'correct_answer', 'points')
    list_filter = ('question_group__section__exam', 'correct_answer')
    search_fields = ('statement',)
    ordering = ('question_group', 'question_number')


@admin.register(YesNoNotGivenQuestion)
class YesNoNotGivenAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'question_group', 'correct_answer', 'points')
    list_filter = ('question_group__section__exam', 'correct_answer')
    search_fields = ('statement',)
    ordering = ('question_group', 'question_number')


@admin.register(SentenceCompletionQuestion)
class SentenceCompletionAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'question_group', 'correct_answer', 'max_words', 'points')
    list_filter = ('question_group__section__exam',)
    search_fields = ('sentence_text', 'correct_answer')
    ordering = ('question_group', 'question_number')


@admin.register(ShortAnswerQuestion)
class ShortAnswerAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'question_group', 'correct_answer', 'max_words', 'points')
    list_filter = ('question_group__section__exam',)
    search_fields = ('question_text', 'correct_answer')
    ordering = ('question_group', 'question_number')


@admin.register(DiagramLabelingQuestion)
class DiagramLabelingAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'question_group', 'label_position', 'correct_answer', 'points')
    list_filter = ('question_group__section__exam',)
    search_fields = ('correct_answer',)
    ordering = ('question_group', 'question_number')


@admin.register(SummaryCompletionQuestion)
class SummaryCompletionAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'question_group', 'has_word_bank', 'correct_answer', 'points')
    list_filter = ('question_group__section__exam', 'has_word_bank')
    search_fields = ('summary_text', 'correct_answer')
    ordering = ('question_group', 'question_number')


@admin.register(ExamLink)
class ExamLinkAdmin(admin.ModelAdmin):
    list_display = ('exam', 'unique_token', 'is_active', 'use_count', 'max_uses', 'expires_at', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('exam__title', 'unique_token')
    readonly_fields = ('unique_token', 'use_count')
    ordering = ('-created_at',)
