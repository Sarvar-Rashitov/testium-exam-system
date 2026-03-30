from django.db import models
from django.conf import settings
import uuid
from django.utils import timezone


class Exam(models.Model):
    """Exam model"""
    organization = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exams')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration = models.IntegerField(help_text='Duration in minutes')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'exams'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Section(models.Model):
    """Section within an exam (e.g., Reading Section 1, Listening Part 2)"""
    MODULE_TYPES = (
        ('reading', 'Reading'),
        ('listening', 'Listening'),
        ('writing', 'Writing'),
        ('speaking', 'Speaking'),
    )
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255, help_text='e.g., "Reading Section 1"')
    module = models.CharField(max_length=20, choices=MODULE_TYPES)
    order = models.IntegerField(default=0)
    
    # Reading specific
    passage_text = models.TextField(blank=True, help_text='Reading passage text')
    
    # Listening specific
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True)
    audio_url = models.URLField(blank=True, null=True)
    
    # Optional image
    image = models.ImageField(upload_to='sections/', null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.exam.title} - {self.title}"


class QuestionGroup(models.Model):
    """Group of questions with same instructions (e.g., Questions 1-5)"""
    QUESTION_TYPE_CHOICES = (
        ('multiple_choice_single', 'Multiple Choice (Single Answer)'),
        ('multiple_choice_multiple', 'Multiple Choice (Multiple Answers)'),
        ('true_false_ng', 'True/False/Not Given'),
        ('yes_no_ng', 'Yes/No/Not Given'),
        ('matching_headings', 'Matching Headings'),
        ('matching_information', 'Matching Information'),
        ('matching_features', 'Matching Features'),
        ('matching_sentence_endings', 'Matching Sentence Endings'),
        ('sentence_completion', 'Sentence Completion'),
        ('summary_completion', 'Summary Completion'),
        ('note_completion', 'Note Completion'),
        ('table_completion', 'Table Completion'),
        ('flowchart_completion', 'Flow-chart Completion'),
        ('diagram_labeling', 'Diagram Labeling'),
        ('short_answer', 'Short Answer'),
    )
    
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='question_groups')
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPE_CHOICES)
    title = models.CharField(max_length=255, help_text='e.g., "Questions 1-5"')
    instructions = models.TextField(help_text='Instructions for this group')
    order = models.IntegerField(default=0)
    
    # Optional specific passage for this group
    passage_text = models.TextField(blank=True)
    image = models.ImageField(upload_to='question_groups/', null=True, blank=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.section} - {self.title}"


# ==================== QUESTION MODELS ====================

class BaseQuestion(models.Model):
    """Abstract base for all questions"""
    question_group = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE, related_name='%(class)s_set')
    question_number = models.IntegerField()
    points = models.IntegerField(default=1)
    explanation = models.TextField(blank=True, help_text='Explanation for the answer')
    
    class Meta:
        abstract = True
        ordering = ['question_number']
    
    def __str__(self):
        return f"Q{self.question_number}"


class MultipleChoiceSingleQuestion(BaseQuestion):
    """Multiple choice with single answer"""
    question_text = models.TextField()
    image = models.ImageField(upload_to='questions/mc/', null=True, blank=True)
    
    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()
    
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    
    class Meta:
        unique_together = ['question_group', 'question_number']
        verbose_name = 'Multiple Choice (Single)'


class MultipleChoiceMultipleQuestion(BaseQuestion):
    """Multiple choice with multiple answers"""
    question_text = models.TextField()
    image = models.ImageField(upload_to='questions/mc/', null=True, blank=True)
    
    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()
    option_e = models.TextField(blank=True)
    option_f = models.TextField(blank=True)
    
    # Store as comma-separated: "A,C,D"
    correct_answers = models.CharField(max_length=50, help_text='Comma-separated: A,B,C')
    
    class Meta:
        unique_together = ['question_group', 'question_number']
        verbose_name = 'Multiple Choice (Multiple)'


class TrueFalseNotGivenQuestion(BaseQuestion):
    """True/False/Not Given"""
    statement = models.TextField()
    correct_answer = models.CharField(max_length=20, choices=[
        ('TRUE', 'True'),
        ('FALSE', 'False'),
        ('NOT GIVEN', 'Not Given')
    ])
    
    class Meta:
        unique_together = ['question_group', 'question_number']


class YesNoNotGivenQuestion(BaseQuestion):
    """Yes/No/Not Given"""
    statement = models.TextField()
    correct_answer = models.CharField(max_length=20, choices=[
        ('YES', 'Yes'),
        ('NO', 'No'),
        ('NOT GIVEN', 'Not Given')
    ])
    
    class Meta:
        unique_together = ['question_group', 'question_number']


class SentenceCompletionQuestion(BaseQuestion):
    """Sentence completion"""
    sentence_text = models.TextField(help_text='Use _____ for blank')
    correct_answer = models.CharField(max_length=255)
    alternative_answers = models.TextField(blank=True, help_text='One per line')
    max_words = models.IntegerField(default=3)
    
    class Meta:
        unique_together = ['question_group', 'question_number']


class ShortAnswerQuestion(BaseQuestion):
    """Short answer"""
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=255)
    alternative_answers = models.TextField(blank=True, help_text='One per line')
    max_words = models.IntegerField(default=3)
    
    class Meta:
        unique_together = ['question_group', 'question_number']


class DiagramLabelingQuestion(BaseQuestion):
    """Diagram labeling"""
    diagram_image = models.ImageField(upload_to='diagrams/')
    label_position = models.CharField(max_length=50, help_text='Position on diagram')
    correct_answer = models.CharField(max_length=255)
    alternative_answers = models.TextField(blank=True, help_text='One per line')
    
    class Meta:
        unique_together = ['question_group', 'question_number']


class SummaryCompletionQuestion(BaseQuestion):
    """Summary completion"""
    summary_text = models.TextField(help_text='Use _____ for blanks')
    has_word_bank = models.BooleanField(default=False)
    correct_answer = models.CharField(max_length=255)
    alternative_answers = models.TextField(blank=True)
    max_words = models.IntegerField(default=2)
    
    class Meta:
        unique_together = ['question_group', 'question_number']


class NoteCompletionQuestion(BaseQuestion):
    """Note completion"""
    note_text = models.TextField(help_text='Use _____ for blank')
    correct_answer = models.CharField(max_length=255)
    alternative_answers = models.TextField(blank=True)
    max_words = models.IntegerField(default=2)
    
    class Meta:
        unique_together = ['question_group', 'question_number']


class TableCompletionQuestion(BaseQuestion):
    """Table completion"""
    row_header = models.CharField(max_length=255, blank=True)
    column_header = models.CharField(max_length=255, blank=True)
    cell_context = models.TextField()
    correct_answer = models.CharField(max_length=255)
    alternative_answers = models.TextField(blank=True)
    max_words = models.IntegerField(default=2)
    
    class Meta:
        unique_together = ['question_group', 'question_number']


class FlowchartCompletionQuestion(BaseQuestion):
    """Flowchart completion"""
    flowchart_image = models.ImageField(upload_to='flowcharts/', null=True, blank=True)
    box_position = models.CharField(max_length=50)
    box_context = models.TextField()
    correct_answer = models.CharField(max_length=255)
    alternative_answers = models.TextField(blank=True)
    max_words = models.IntegerField(default=2)
    
    class Meta:
        unique_together = ['question_group', 'question_number']


# ==================== MATCHING QUESTIONS ====================

class MatchingHeadingsQuestion(BaseQuestion):
    """Matching headings to paragraphs"""
    paragraph_label = models.CharField(max_length=10, help_text='A, B, C, etc.')
    correct_heading = models.CharField(max_length=10, help_text='i, ii, iii, etc.')
    
    class Meta:
        unique_together = ['question_group', 'question_number']


class HeadingOption(models.Model):
    """Heading options for matching"""
    question_group = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE, related_name='heading_options')
    heading_label = models.CharField(max_length=10)
    heading_text = models.TextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']


class MatchingInformationQuestion(BaseQuestion):
    """Match information to paragraphs"""
    information_text = models.TextField()
    correct_paragraph = models.CharField(max_length=10, help_text='A, B, C, etc.')
    
    class Meta:
        unique_together = ['question_group', 'question_number']


class MatchingFeaturesQuestion(BaseQuestion):
    """Match features (names to statements)"""
    statement = models.TextField()
    correct_feature = models.CharField(max_length=10, help_text='A, B, C, etc.')
    
    class Meta:
        unique_together = ['question_group', 'question_number']


class FeatureOption(models.Model):
    """Feature options"""
    question_group = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE, related_name='feature_options')
    feature_label = models.CharField(max_length=10)
    feature_text = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']


class MatchingSentenceEndingsQuestion(BaseQuestion):
    """Match sentence endings"""
    sentence_start = models.TextField()
    correct_ending = models.CharField(max_length=10, help_text='A, B, C, etc.')
    
    class Meta:
        unique_together = ['question_group', 'question_number']


class SentenceEndingOption(models.Model):
    """Sentence ending options"""
    question_group = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE, related_name='ending_options')
    ending_label = models.CharField(max_length=10)
    ending_text = models.TextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']


# ==================== EXAM LINKS ====================

class ExamLink(models.Model):
    """Unique exam link"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='links')
    unique_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    max_uses = models.IntegerField(null=True, blank=True)
    use_count = models.IntegerField(default=0)
    resume_password = models.CharField(max_length=50, blank=True, null=True, help_text='Parol imtihonni davom ettirish uchun')
    
    class Meta:
        db_table = 'exam_links'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.exam.title} - {self.unique_token}"
    
    def is_valid(self):
        if not self.is_active:
            return False
        if self.expires_at and timezone.now() > self.expires_at:
            return False
        if self.max_uses and self.use_count >= self.max_uses:
            return False
        return True
    
    def get_full_url(self, request=None):
        """Get full exam URL"""
        if request:
            return request.build_absolute_uri(f'/exam/start/{self.unique_token}/')
        return f'/exam/start/{self.unique_token}/'
