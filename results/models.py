from django.db import models
from exams.models import Exam, ExamLink
from students.models import Student


class Result(models.Model):
    """Result model"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    exam_link = models.ForeignKey(ExamLink, on_delete=models.SET_NULL, null=True, related_name='results')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    total_points = models.IntegerField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    answers = models.JSONField(default=dict, help_text='JSON format: {"question_id": "answer"}')
    time_taken = models.IntegerField(help_text='Time taken in seconds', null=True, blank=True)
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(auto_now_add=True)
    tab_switches = models.IntegerField(default=0, help_text='Number of times student switched tabs')
    
    class Meta:
        db_table = 'results'
        ordering = ['-completed_at']
        indexes = [
            models.Index(fields=['exam', '-completed_at']),
            models.Index(fields=['student', '-completed_at']),
        ]
    
    def __str__(self):
        return f"{self.student.full_name} - {self.exam.title} - {self.score}"
    
    @property
    def band_score(self):
        """Calculate IELTS band score (0-9)"""
        if self.percentage >= 90:
            return 9.0
        elif self.percentage >= 80:
            return 8.0
        elif self.percentage >= 70:
            return 7.0
        elif self.percentage >= 60:
            return 6.0
        elif self.percentage >= 50:
            return 5.0
        elif self.percentage >= 40:
            return 4.0
        elif self.percentage >= 30:
            return 3.0
        elif self.percentage >= 20:
            return 2.0
        elif self.percentage >= 10:
            return 1.0
        return 0.0
