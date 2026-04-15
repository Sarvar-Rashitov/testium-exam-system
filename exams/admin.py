from django.contrib import admin
from .models import (
    Exam, Section, QuestionGroup, ExamLink,
    MultipleChoiceSingleQuestion, MultipleChoiceMultipleQuestion,
    TrueFalseNotGivenQuestion, YesNoNotGivenQuestion,
    SentenceCompletionQuestion, ShortAnswerQuestion,
    DiagramLabelingQuestion, ImageLabel, SummaryCompletionQuestion,
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
    list_display = ('title', 'section', 'question_type', 'order', 'get_question_count')
    list_filter = ('question_type', 'section__module')
    search_fields = ('title', 'instructions')
    ordering = ('section', 'order')
    inlines = []
    
    def get_question_count(self, obj):
        """Count questions in this group"""
        count = 0
        if obj.question_type == 'multiple_choice_single':
            count = obj.multiplechoicesinglequestion_set.count()
        elif obj.question_type == 'multiple_choice_multiple':
            count = obj.multiplechoicemultiplequestion_set.count()
        elif obj.question_type == 'true_false_ng':
            count = obj.truefalsenotgivenquestion_set.count()
        elif obj.question_type == 'yes_no_ng':
            count = obj.yesnonotgivenquestion_set.count()
        elif obj.question_type == 'sentence_completion':
            count = obj.sentencecompletionquestion_set.count()
        elif obj.question_type == 'short_answer':
            count = obj.shortanswerquestion_set.count()
        elif obj.question_type == 'diagram_labeling':
            count = obj.diagramlabelingquestion_set.count()
        elif obj.question_type == 'summary_completion':
            count = obj.summarycompletionquestion_set.count()
        elif obj.question_type == 'note_completion':
            count = obj.notecompletionquestion_set.count()
        elif obj.question_type == 'table_completion':
            count = obj.tablecompletionquestion_set.count()
        elif obj.question_type == 'flowchart_completion':
            count = obj.flowchartcompletionquestion_set.count()
        elif obj.question_type == 'matching_headings':
            count = obj.matchingheadingsquestion_set.count()
        elif obj.question_type == 'matching_information':
            count = obj.matchinginformationquestion_set.count()
        elif obj.question_type == 'matching_features':
            count = obj.matchingfeaturesquestion_set.count()
        elif obj.question_type == 'matching_sentence_endings':
            count = obj.matchingsentenceendingsquestion_set.count()
        return count
    get_question_count.short_description = 'Questions'
    
    def get_inline_instances(self, request, obj=None):
        """Dynamically add inlines based on question type"""
        inlines = []
        if obj:
            if obj.question_type == 'matching_headings':
                inlines.append(HeadingOptionInline(self.model, self.admin_site))
            elif obj.question_type == 'matching_features':
                inlines.append(FeatureOptionInline(self.model, self.admin_site))
            elif obj.question_type == 'matching_sentence_endings':
                inlines.append(SentenceEndingOptionInline(self.model, self.admin_site))
        return inlines


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


class ImageLabelInline(admin.TabularInline):
    model = ImageLabel
    extra = 1
    fields = ('label_number', 'correct_answer', 'alternative_answers')


class HeadingOptionInline(admin.TabularInline):
    model = HeadingOption
    extra = 3
    fields = ('heading_label', 'heading_text', 'order')


class FeatureOptionInline(admin.TabularInline):
    model = FeatureOption
    extra = 3
    fields = ('feature_label', 'feature_text', 'order')


class SentenceEndingOptionInline(admin.TabularInline):
    model = SentenceEndingOption
    extra = 3
    fields = ('ending_label', 'ending_text', 'order')


@admin.register(DiagramLabelingQuestion)
class DiagramLabelingAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'question_group', 'get_label_count', 'points')
    list_filter = ('question_group__section__exam',)
    inlines = [ImageLabelInline]
    ordering = ('question_group', 'question_number')
    
    def get_label_count(self, obj):
        return obj.labels.count()
    get_label_count.short_description = 'Labels'


@admin.register(SummaryCompletionQuestion)
class SummaryCompletionAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'question_group', 'has_word_bank', 'correct_answer', 'points')
    list_filter = ('question_group__section__exam', 'has_word_bank')
    search_fields = ('summary_text', 'correct_answer')
    ordering = ('question_group', 'question_number')


@admin.register(NoteCompletionQuestion)
class NoteCompletionAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'question_group', 'correct_answer', 'max_words', 'points')
    list_filter = ('question_group__section__exam',)
    search_fields = ('note_text', 'correct_answer')
    ordering = ('question_group', 'question_number')


@admin.register(TableCompletionQuestion)
class TableCompletionAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'question_group', 'row_header', 'column_header', 'correct_answer', 'points')
    list_filter = ('question_group__section__exam',)
    search_fields = ('cell_context', 'correct_answer')
    ordering = ('question_group', 'question_number')


@admin.register(FlowchartCompletionQuestion)
class FlowchartCompletionAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'question_group', 'box_position', 'correct_answer', 'points')
    list_filter = ('question_group__section__exam',)
    search_fields = ('box_context', 'correct_answer')
    ordering = ('question_group', 'question_number')


@admin.register(MatchingHeadingsQuestion)
class MatchingHeadingsAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'question_group', 'paragraph_label', 'correct_heading', 'points')
    list_filter = ('question_group__section__exam',)
    search_fields = ('paragraph_label', 'correct_heading')
    ordering = ('question_group', 'question_number')


@admin.register(HeadingOption)
class HeadingOptionAdmin(admin.ModelAdmin):
    list_display = ('question_group', 'heading_label', 'heading_text', 'order')
    list_filter = ('question_group__section__exam',)
    search_fields = ('heading_label', 'heading_text')
    ordering = ('question_group', 'order')


@admin.register(MatchingInformationQuestion)
class MatchingInformationAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'question_group', 'correct_paragraph', 'points')
    list_filter = ('question_group__section__exam',)
    search_fields = ('information_text', 'correct_paragraph')
    ordering = ('question_group', 'question_number')


@admin.register(MatchingFeaturesQuestion)
class MatchingFeaturesAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'question_group', 'correct_feature', 'points')
    list_filter = ('question_group__section__exam',)
    search_fields = ('statement', 'correct_feature')
    ordering = ('question_group', 'question_number')


@admin.register(FeatureOption)
class FeatureOptionAdmin(admin.ModelAdmin):
    list_display = ('question_group', 'feature_label', 'feature_text', 'order')
    list_filter = ('question_group__section__exam',)
    search_fields = ('feature_label', 'feature_text')
    ordering = ('question_group', 'order')


@admin.register(MatchingSentenceEndingsQuestion)
class MatchingSentenceEndingsAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'question_group', 'correct_ending', 'points')
    list_filter = ('question_group__section__exam',)
    search_fields = ('sentence_start', 'correct_ending')
    ordering = ('question_group', 'question_number')


@admin.register(SentenceEndingOption)
class SentenceEndingOptionAdmin(admin.ModelAdmin):
    list_display = ('question_group', 'ending_label', 'ending_text', 'order')
    list_filter = ('question_group__section__exam',)
    search_fields = ('ending_label', 'ending_text')
    ordering = ('question_group', 'order')


@admin.register(ImageLabel)
class ImageLabelAdmin(admin.ModelAdmin):
    list_display = ('question', 'label_number', 'correct_answer')
    list_filter = ('question__question_group__section__exam',)
    search_fields = ('correct_answer',)
    ordering = ('question', 'label_number')


@admin.register(ExamLink)
class ExamLinkAdmin(admin.ModelAdmin):
    list_display = ('exam', 'unique_token', 'is_active', 'use_count', 'max_uses', 'expires_at', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('exam__title', 'unique_token')
    readonly_fields = ('unique_token', 'use_count')
    ordering = ('-created_at',)
