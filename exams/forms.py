from django import forms
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


class ExamForm(forms.ModelForm):
    """Exam creation/edit form"""
    class Meta:
        model = Exam
        fields = ('title', 'description', 'duration', 'is_active')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Imtihon nomi'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Imtihon haqida ma\'lumot'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Davomiyligi (daqiqalarda)',
                'min': 1
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class SectionForm(forms.ModelForm):
    """Section form"""
    class Meta:
        model = Section
        fields = ('title', 'module', 'passage_text', 'audio_file', 'audio_url', 'image', 'order', 'is_active')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Reading Section 1'}),
            'module': forms.Select(attrs={'class': 'form-control'}),
            'passage_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Reading passage matni'}),
            'audio_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Audio URL'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'value': 0}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class QuestionGroupForm(forms.ModelForm):
    """Question group form"""
    class Meta:
        model = QuestionGroup
        fields = ('question_type', 'title', 'instructions', 'passage_text', 'image', 'order')
        widgets = {
            'question_type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Questions 1-5'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ko\'rsatmalar'}),
            'passage_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Agar kerak bo\'lsa'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'value': 0})
        }


# ==================== QUESTION FORMS ====================

class MultipleChoiceSingleForm(forms.ModelForm):
    """Multiple choice single answer form"""
    class Meta:
        model = MultipleChoiceSingleQuestion
        fields = ('question_number', 'question_text', 'image', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'points', 'explanation')
        widgets = {
            'question_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'option_a': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'A variant'}),
            'option_b': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'B variant'}),
            'option_c': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'C variant'}),
            'option_d': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'D variant'}),
            'correct_answer': forms.Select(attrs={'class': 'form-control'}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ixtiyoriy'})
        }


class MultipleChoiceMultipleForm(forms.ModelForm):
    """Multiple choice multiple answers form"""
    class Meta:
        model = MultipleChoiceMultipleQuestion
        fields = ('question_number', 'question_text', 'image', 'option_a', 'option_b', 'option_c', 'option_d', 'option_e', 'option_f', 'correct_answers', 'points', 'explanation')
        widgets = {
            'question_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'option_a': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'A variant'}),
            'option_b': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'B variant'}),
            'option_c': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'C variant'}),
            'option_d': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'D variant'}),
            'option_e': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E variant (ixtiyoriy)'}),
            'option_f': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'F variant (ixtiyoriy)'}),
            'correct_answers': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: A,C,D'}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ixtiyoriy'})
        }


class TrueFalseNotGivenForm(forms.ModelForm):
    """True/False/Not Given form"""
    class Meta:
        model = TrueFalseNotGivenQuestion
        fields = ('question_number', 'statement', 'correct_answer', 'points', 'explanation')
        widgets = {
            'question_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'statement': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'correct_answer': forms.Select(attrs={'class': 'form-control'}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ixtiyoriy'})
        }


class YesNoNotGivenForm(forms.ModelForm):
    """Yes/No/Not Given form"""
    class Meta:
        model = YesNoNotGivenQuestion
        fields = ('question_number', 'statement', 'correct_answer', 'points', 'explanation')
        widgets = {
            'question_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'statement': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'correct_answer': forms.Select(attrs={'class': 'form-control'}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ixtiyoriy'})
        }


class SentenceCompletionForm(forms.ModelForm):
    """Sentence completion form"""
    class Meta:
        model = SentenceCompletionQuestion
        fields = ('question_number', 'sentence_text', 'correct_answer', 'alternative_answers', 'max_words', 'points', 'explanation')
        widgets = {
            'question_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'sentence_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Bo\'sh joy uchun _____ ishlating'}),
            'correct_answer': forms.TextInput(attrs={'class': 'form-control'}),
            'alternative_answers': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Har bir qatorda bitta (ixtiyoriy)'}),
            'max_words': forms.NumberInput(attrs={'class': 'form-control', 'value': 3}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ixtiyoriy'})
        }


class ShortAnswerForm(forms.ModelForm):
    """Short answer form"""
    class Meta:
        model = ShortAnswerQuestion
        fields = ('question_number', 'question_text', 'correct_answer', 'alternative_answers', 'max_words', 'points', 'explanation')
        widgets = {
            'question_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'correct_answer': forms.TextInput(attrs={'class': 'form-control'}),
            'alternative_answers': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Har bir qatorda bitta (ixtiyoriy)'}),
            'max_words': forms.NumberInput(attrs={'class': 'form-control', 'value': 3}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ixtiyoriy'})
        }


class DiagramLabelingForm(forms.ModelForm):
    """Diagram labeling form - main question"""
    class Meta:
        model = DiagramLabelingQuestion
        fields = ('question_number', 'diagram_image', 'instruction', 'points', 'explanation')
        widgets = {
            'question_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'instruction': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Label the diagram below'}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ixtiyoriy'})
        }


class ImageLabelForm(forms.ModelForm):
    """Form for individual label in diagram/map/table"""
    class Meta:
        model = ImageLabel
        fields = ('label_number', 'correct_answer', 'alternative_answers')
        widgets = {
            'label_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Rasm ichidagi raqam'}),
            'correct_answer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'To\'g\'ri javob'}),
            'alternative_answers': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Har bir qatorda bitta (ixtiyoriy)'})
        }


# Formset for managing multiple labels
from django.forms import inlineformset_factory

ImageLabelFormSet = inlineformset_factory(
    DiagramLabelingQuestion,
    ImageLabel,
    form=ImageLabelForm,
    extra=3,
    can_delete=True,
    min_num=1,
    validate_min=True
)


class SummaryCompletionForm(forms.ModelForm):
    """Summary completion form"""
    class Meta:
        model = SummaryCompletionQuestion
        fields = ('question_number', 'summary_text', 'has_word_bank', 'correct_answer', 'alternative_answers', 'max_words', 'points', 'explanation')
        widgets = {
            'question_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'summary_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Bo\'sh joy uchun _____ ishlating'}),
            'has_word_bank': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'correct_answer': forms.TextInput(attrs={'class': 'form-control'}),
            'alternative_answers': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Har bir qatorda bitta (ixtiyoriy)'}),
            'max_words': forms.NumberInput(attrs={'class': 'form-control', 'value': 2}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ixtiyoriy'})
        }


class ExamLinkForm(forms.ModelForm):
    """Exam link generation form"""
    expires_in_days = forms.IntegerField(
        required=False,
        initial=30,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Amal qilish muddati (kunlarda)'
        })
    )
    
    class Meta:
        model = ExamLink
        fields = ('max_uses', 'resume_password', 'is_active')
        widgets = {
            'max_uses': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Maksimal foydalanish soni (bo\'sh = cheksiz)'
            }),
            'resume_password': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Davom ettirish paroli (masalan: 1234)'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class NoteCompletionForm(forms.ModelForm):
    """Note completion form"""
    class Meta:
        model = NoteCompletionQuestion
        fields = ('question_number', 'note_text', 'correct_answer', 'alternative_answers', 'max_words', 'points', 'explanation')
        widgets = {
            'question_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'note_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Bo\'sh joy uchun _____ ishlating'}),
            'correct_answer': forms.TextInput(attrs={'class': 'form-control'}),
            'alternative_answers': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Har bir qatorda bitta (ixtiyoriy)'}),
            'max_words': forms.NumberInput(attrs={'class': 'form-control', 'value': 2}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ixtiyoriy'})
        }


class TableCompletionForm(forms.ModelForm):
    """Table completion form"""
    class Meta:
        model = TableCompletionQuestion
        fields = ('question_number', 'row_header', 'column_header', 'cell_context', 'correct_answer', 'alternative_answers', 'max_words', 'points', 'explanation')
        widgets = {
            'question_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'row_header': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Qator sarlavhasi'}),
            'column_header': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ustun sarlavhasi'}),
            'cell_context': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Katak konteksti'}),
            'correct_answer': forms.TextInput(attrs={'class': 'form-control'}),
            'alternative_answers': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Har bir qatorda bitta (ixtiyoriy)'}),
            'max_words': forms.NumberInput(attrs={'class': 'form-control', 'value': 2}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ixtiyoriy'})
        }


class FlowchartCompletionForm(forms.ModelForm):
    """Flowchart completion form"""
    class Meta:
        model = FlowchartCompletionQuestion
        fields = ('question_number', 'flowchart_image', 'box_position', 'box_context', 'correct_answer', 'alternative_answers', 'max_words', 'points', 'explanation')
        widgets = {
            'question_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'box_position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quti pozitsiyasi'}),
            'box_context': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Quti konteksti'}),
            'correct_answer': forms.TextInput(attrs={'class': 'form-control'}),
            'alternative_answers': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Har bir qatorda bitta (ixtiyoriy)'}),
            'max_words': forms.NumberInput(attrs={'class': 'form-control', 'value': 2}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ixtiyoriy'})
        }


class MatchingHeadingsForm(forms.ModelForm):
    """Matching headings form"""
    class Meta:
        model = MatchingHeadingsQuestion
        fields = ('question_number', 'paragraph_label', 'correct_heading', 'points', 'explanation')
        widgets = {
            'question_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'paragraph_label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'A, B, C...'}),
            'correct_heading': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'i, ii, iii...'}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ixtiyoriy'})
        }


class MatchingInformationForm(forms.ModelForm):
    """Matching information form"""
    class Meta:
        model = MatchingInformationQuestion
        fields = ('question_number', 'information_text', 'correct_paragraph', 'points', 'explanation')
        widgets = {
            'question_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'information_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'correct_paragraph': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'A, B, C...'}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ixtiyoriy'})
        }


class MatchingFeaturesForm(forms.ModelForm):
    """Matching features form"""
    class Meta:
        model = MatchingFeaturesQuestion
        fields = ('question_number', 'statement', 'correct_feature', 'points', 'explanation')
        widgets = {
            'question_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'statement': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'correct_feature': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'A, B, C...'}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ixtiyoriy'})
        }


class MatchingSentenceEndingsForm(forms.ModelForm):
    """Matching sentence endings form"""
    class Meta:
        model = MatchingSentenceEndingsQuestion
        fields = ('question_number', 'sentence_start', 'correct_ending', 'points', 'explanation')
        widgets = {
            'question_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'sentence_start': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'correct_ending': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'A, B, C...'}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ixtiyoriy'})
        }
