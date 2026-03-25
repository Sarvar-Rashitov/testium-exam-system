from django.db import models
from django.conf import settings
import uuid
from datetime import timedelta
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


class Question(models.Model):
    """Universal Question model for all IELTS question types"""
    
    # IELTS Question Types
    QUESTION_TYPES = (
        # Multiple Choice
        ('mcq_single', 'Multiple Choice (Single Answer)'),
        ('mcq_multiple', 'Multiple Choice (Multiple Answers)'),
        
        # True/False/Not Given
        ('true_false_ng', 'True / False / Not Given'),
        ('yes_no_ng', 'Yes / No / Not Given'),
        
        # Matching Types
        ('matching_headings', 'Matching Headings'),
        ('matching_information', 'Matching Information'),
        ('matching_features', 'Matching Features'),
        ('matching_sentence_endings', 'Matching Sentence Endings'),
        
        # Completion Types
        ('sentence_completion', 'Sentence Completion'),
        ('summary_completion', 'Summary Completion'),
        ('note_completion', 'Note Completion'),
        ('table_completion', 'Table Completion'),
        ('flowchart_completion', 'Flow-chart Completion'),
        ('diagram_labeling', 'Diagram Label Completion'),
        
        # Short Answer
        ('short_answer', 'Short Answer Questions'),
        
        # Writing (existing)
        ('writing', 'Writing Task'),
    )
    
    # Module Types
    MODULE_TYPES = (
        ('reading', 'Reading'),
        ('listening', 'Listening'),
        ('writing', 'Writing'),
        ('speaking', 'Speaking'),
    )
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    module = models.CharField(max_length=20, choices=MODULE_TYPES, default='reading')
    type = models.CharField(max_length=30, choices=QUESTION_TYPES)
    
    # Universal fields
    instruction_text = models.TextField(help_text='Instructions for this question')
    content = models.JSONField(default=dict, help_text='Question content (structure varies by type)')
    correct_answer = models.JSONField(default=dict, help_text='Correct answer(s) in JSON format')
    explanation = models.TextField(blank=True, help_text='Explanation for the answer')
    
    # Listening specific
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True, help_text='Audio file for listening questions')
    audio_url = models.URLField(blank=True, null=True, help_text='Audio file URL (alternative to file upload)')
    start_time = models.IntegerField(null=True, blank=True, help_text='Audio start time in seconds')
    end_time = models.IntegerField(null=True, blank=True, help_text='Audio end time in seconds')
    
    # Image for diagrams
    image_file = models.ImageField(upload_to='images/', blank=True, null=True, help_text='Image file for diagram questions')
    image_url = models.URLField(blank=True, null=True, help_text='Image URL (alternative to file upload)')
    
    # Metadata
    order = models.IntegerField(default=0, help_text='Display order')
    points = models.IntegerField(default=1, help_text='Points for this question')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'questions'
        ordering = ['order', 'id']
        indexes = [
            models.Index(fields=['exam', 'module', 'order']),
            models.Index(fields=['type']),
        ]
    
    def __str__(self):
        return f"{self.exam.title} - {self.get_module_display()} - Q{self.order}"
    
    def validate_content(self):
        """Validate content structure based on question type"""
        validators = {
            'mcq_single': self._validate_mcq,
            'mcq_multiple': self._validate_mcq,
            'true_false_ng': self._validate_statement,
            'yes_no_ng': self._validate_statement,
            'matching_headings': self._validate_matching_headings,
            'matching_information': self._validate_matching_info,
            'matching_features': self._validate_matching_features,
            'matching_sentence_endings': self._validate_matching_endings,
            'sentence_completion': self._validate_completion,
            'summary_completion': self._validate_summary,
            'note_completion': self._validate_summary,
            'table_completion': self._validate_table,
            'flowchart_completion': self._validate_flowchart,
            'diagram_labeling': self._validate_diagram,
            'short_answer': self._validate_short_answer,
        }
        
        validator = validators.get(self.type)
        if validator:
            return validator()
        return True
    
    def _validate_mcq(self):
        """Validate MCQ content"""
        required = ['question', 'options']
        return all(key in self.content for key in required)
    
    def _validate_statement(self):
        """Validate True/False/Not Given content"""
        return 'statement' in self.content
    
    def _validate_matching_headings(self):
        """Validate Matching Headings content"""
        required = ['paragraphs', 'headings']
        return all(key in self.content for key in required)
    
    def _validate_matching_info(self):
        """Validate Matching Information content"""
        required = ['statements', 'paragraphs']
        return all(key in self.content for key in required)
    
    def _validate_matching_features(self):
        """Validate Matching Features content"""
        required = ['statements', 'features']
        return all(key in self.content for key in required)
    
    def _validate_matching_endings(self):
        """Validate Matching Sentence Endings content"""
        required = ['sentence_beginnings', 'sentence_endings']
        return all(key in self.content for key in required)
    
    def _validate_completion(self):
        """Validate Sentence Completion content"""
        return 'sentence' in self.content
    
    def _validate_summary(self):
        """Validate Summary/Note Completion content"""
        required = ['text', 'fields']
        return all(key in self.content for key in required)
    
    def _validate_table(self):
        """Validate Table Completion content"""
        required = ['table_data', 'fields']
        return all(key in self.content for key in required)
    
    def _validate_flowchart(self):
        """Validate Flowchart Completion content"""
        required = ['flowchart_data', 'fields']
        return all(key in self.content for key in required)
    
    def _validate_diagram(self):
        """Validate Diagram Labeling content"""
        required = ['image_url', 'labels']
        return all(key in self.content for key in required)
    
    def _validate_short_answer(self):
        """Validate Short Answer content"""
        required = ['question', 'word_limit']
        return all(key in self.content for key in required)
    
    def check_answer(self, student_answer):
        """Check if student answer is correct"""
        if self.type in ['mcq_single', 'true_false_ng', 'yes_no_ng']:
            return self._check_single_answer(student_answer)
        elif self.type == 'mcq_multiple':
            return self._check_multiple_answers(student_answer)
        elif self.type in ['matching_headings', 'matching_information', 'matching_features', 'matching_sentence_endings']:
            return self._check_matching(student_answer)
        elif self.type in ['sentence_completion', 'summary_completion', 'note_completion', 'table_completion', 'flowchart_completion', 'diagram_labeling', 'short_answer']:
            return self._check_completion(student_answer)
        return False
    
    def _check_single_answer(self, student_answer):
        """Check single answer"""
        correct = str(self.correct_answer.get('answer', '')).strip().upper()
        student = str(student_answer).strip().upper()
        return correct == student
    
    def _check_multiple_answers(self, student_answer):
        """Check multiple answers"""
        correct = set(str(a).strip().upper() for a in self.correct_answer.get('answers', []))
        student = set(str(a).strip().upper() for a in student_answer) if isinstance(student_answer, list) else set()
        return correct == student
    
    def _check_matching(self, student_answer):
        """Check matching answers"""
        if not isinstance(student_answer, dict):
            return False
        correct = self.correct_answer
        matches = 0
        for key, value in correct.items():
            if str(student_answer.get(key, '')).strip() == str(value).strip():
                matches += 1
        return matches == len(correct)
    
    def _check_completion(self, student_answer):
        """Check completion answers (case-insensitive, trimmed)"""
        if not isinstance(student_answer, dict):
            return False
        correct = self.correct_answer
        matches = 0
        for key, value in correct.items():
            student_val = str(student_answer.get(key, '')).strip().lower()
            correct_val = str(value).strip().lower()
            if student_val == correct_val:
                matches += 1
        return matches == len(correct)


class ExamLink(models.Model):
    """Unique exam link model"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='links')
    unique_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    max_uses = models.IntegerField(null=True, blank=True, help_text='Maximum number of uses (null = unlimited)')
    use_count = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'exam_links'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.exam.title} - {self.unique_token}"
    
    def is_valid(self):
        """Check if link is still valid"""
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
