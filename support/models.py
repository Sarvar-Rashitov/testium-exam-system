from django.db import models


class SupportVideo(models.Model):
    """Support videos for helping users"""
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    video_url = models.URLField(verbose_name="Video URL (YouTube, Vimeo)")
    thumbnail = models.ImageField(upload_to='support/thumbnails/', blank=True, null=True, verbose_name="Rasm")
    category = models.CharField(max_length=100, choices=[
        ('getting_started', 'Boshlash'),
        ('exams', 'Imtihonlar'),
        ('students', 'Talabalar'),
        ('results', 'Natijalar'),
        ('settings', 'Sozlamalar'),
        ('other', 'Boshqa'),
    ], default='other', verbose_name="Kategoriya")
    duration = models.CharField(max_length=20, blank=True, verbose_name="Davomiyligi")
    order = models.IntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'support_videos'
        ordering = ['order', '-created_at']
        verbose_name = 'Yordam videosi'
        verbose_name_plural = 'Yordam videolari'
    
    def __str__(self):
        return self.title


class FAQ(models.Model):
    """Frequently Asked Questions"""
    question = models.CharField(max_length=500, verbose_name="Savol")
    answer = models.TextField(verbose_name="Javob")
    category = models.CharField(max_length=100, choices=[
        ('general', 'Umumiy'),
        ('exams', 'Imtihonlar'),
        ('students', 'Talabalar'),
        ('results', 'Natijalar'),
        ('technical', 'Texnik'),
        ('billing', 'To\'lov'),
    ], default='general', verbose_name="Kategoriya")
    order = models.IntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    views = models.IntegerField(default=0, verbose_name="Ko'rishlar soni")
    helpful_count = models.IntegerField(default=0, verbose_name="Foydali deb belgilangan")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'faqs'
        ordering = ['order', '-helpful_count']
        verbose_name = 'Ko\'p beriladigan savol'
        verbose_name_plural = 'Ko\'p beriladigan savollar'
    
    def __str__(self):
        return self.question


class ContactInfo(models.Model):
    """Platform contact information"""
    title = models.CharField(max_length=100, verbose_name="Sarlavha")
    description = models.TextField(verbose_name="Tavsif")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    telegram = models.CharField(max_length=100, blank=True, verbose_name="Telegram")
    address = models.TextField(blank=True, verbose_name="Manzil")
    working_hours = models.CharField(max_length=200, blank=True, verbose_name="Ish vaqti")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'contact_info'
        verbose_name = 'Aloqa ma\'lumotlari'
        verbose_name_plural = 'Aloqa ma\'lumotlari'
    
    def __str__(self):
        return self.title


class SupportTicket(models.Model):
    """Support tickets from organizations"""
    from organizations.models import Organization
    
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='support_tickets')
    subject = models.CharField(max_length=255, verbose_name="Mavzu")
    message = models.TextField(verbose_name="Xabar")
    category = models.CharField(max_length=100, choices=[
        ('technical', 'Texnik muammo'),
        ('billing', 'To\'lov'),
        ('feature', 'Yangi funksiya'),
        ('bug', 'Xatolik'),
        ('other', 'Boshqa'),
    ], default='other', verbose_name="Kategoriya")
    status = models.CharField(max_length=50, choices=[
        ('open', 'Ochiq'),
        ('in_progress', 'Jarayonda'),
        ('resolved', 'Hal qilindi'),
        ('closed', 'Yopildi'),
    ], default='open', verbose_name="Holat")
    priority = models.CharField(max_length=50, choices=[
        ('low', 'Past'),
        ('medium', 'O\'rta'),
        ('high', 'Yuqori'),
        ('urgent', 'Shoshilinch'),
    ], default='medium', verbose_name="Muhimlik")
    attachment = models.FileField(upload_to='support/attachments/', blank=True, null=True, verbose_name="Fayl")
    admin_response = models.TextField(blank=True, verbose_name="Admin javobi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(blank=True, null=True, verbose_name="Hal qilingan vaqt")
    
    class Meta:
        db_table = 'support_tickets'
        ordering = ['-created_at']
        verbose_name = 'Yordam so\'rovi'
        verbose_name_plural = 'Yordam so\'rovlari'
    
    def __str__(self):
        return f"{self.organization.organization_name} - {self.subject}"


class TeamMember(models.Model):
    """Testium team members"""
    name = models.CharField(max_length=100, verbose_name="Ism")
    position = models.CharField(max_length=100, verbose_name="Lavozim")
    bio = models.TextField(blank=True, verbose_name="Biografiya")
    photo = models.ImageField(upload_to='team/', blank=True, null=True, verbose_name="Rasm")
    email = models.EmailField(blank=True, verbose_name="Email")
    telegram = models.CharField(max_length=100, blank=True, verbose_name="Telegram")
    linkedin = models.URLField(blank=True, verbose_name="LinkedIn")
    order = models.IntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'team_members'
        ordering = ['order', 'name']
        verbose_name = 'Jamoa a\'zosi'
        verbose_name_plural = 'Jamoa a\'zolari'
    
    def __str__(self):
        return f"{self.name} - {self.position}"
