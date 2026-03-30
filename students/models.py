from django.db import models


class Student(models.Model):
    """Student model - no authentication required"""
    STUDENT_TYPE_CHOICES = [
        ('institution', 'Muassasa o\'quvchisi'),
        ('external', 'Tashqi o\'quvchi'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    telegram_username = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    student_type = models.CharField(max_length=20, choices=STUDENT_TYPE_CHOICES, default='external')
    teacher = models.ForeignKey('organizations.Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='students', verbose_name="O'qituvchi")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'students'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
