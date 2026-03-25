from django import forms
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
    """Diagram labeling form"""
    class Meta:
        model = DiagramLabelingQuestion
        fields = ('question_number', 'diagram_image', 'label_position', 'correct_answer', 'alternative_answers', 'points', 'explanation')
        widgets = {
            'question_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'label_position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: top-left, center'}),
            'correct_answer': forms.TextInput(attrs={'class': 'form-control'}),
            'alternative_answers': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Har bir qatorda bitta (ixtiyoriy)'}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'value': 1}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ixtiyoriy'})
        }


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
        fields = ('max_uses', 'is_active')
        widgets = {
            'max_uses': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Maksimal foydalanish soni (bo\'sh = cheksiz)'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
