from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class Organization(AbstractUser):
    """Organization model - extends Django User for authentication"""
    full_name = models.CharField(max_length=255, default='User')
    organization_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Use email as the username field for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'organization_name']
    
    class Meta:
        db_table = 'organizations'
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
    
    def __str__(self):
        return self.organization_name


class OrganizationSettings(models.Model):
    """Organization settings and customization"""
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, related_name='settings')
    
    # Branding
    logo = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name="Logo", help_text="Barcha rasm formatlari qabul qilinadi")
    primary_color = models.CharField(max_length=7, default='#4F46E5', verbose_name="Asosiy rang")
    secondary_color = models.CharField(max_length=7, default='#10b981', verbose_name="Ikkinchi rang")
    
    # Contact Information
    address = models.TextField(blank=True, verbose_name="Manzil")
    website = models.URLField(blank=True, verbose_name="Veb-sayt")
    telegram = models.CharField(max_length=100, blank=True, verbose_name="Telegram")
    instagram = models.CharField(max_length=100, blank=True, verbose_name="Instagram")
    facebook = models.CharField(max_length=100, blank=True, verbose_name="Facebook")
    
    # Platform Settings
    allow_student_registration = models.BooleanField(default=True, verbose_name="Talaba ro'yxatdan o'tishiga ruxsat")
    show_leaderboard = models.BooleanField(default=True, verbose_name="Reyting jadvalini ko'rsatish")
    enable_certificates = models.BooleanField(default=True, verbose_name="Sertifikatlarni yoqish")
    
    # Notifications
    email_notifications = models.BooleanField(default=True, verbose_name="Email xabarnomalar")
    telegram_notifications = models.BooleanField(default=False, verbose_name="Telegram xabarnomalar")
    telegram_bot_token = models.CharField(max_length=200, blank=True, verbose_name="Telegram bot token")
    
    # About
    about_text = models.TextField(blank=True, verbose_name="Biz haqimizda")
    mission = models.TextField(blank=True, verbose_name="Missiya")
    vision = models.TextField(blank=True, verbose_name="Viziya")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'organization_settings'
        verbose_name = 'Tashkilot sozlamalari'
        verbose_name_plural = 'Tashkilot sozlamalari'
    
    def __str__(self):
        return f"{self.organization.organization_name} - Sozlamalar"


class Teacher(models.Model):
    """Teacher model for organization"""
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='teachers')
    first_name = models.CharField(max_length=100, verbose_name="Ism")
    last_name = models.CharField(max_length=100, verbose_name="Familiya")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="Email")
    subject = models.CharField(max_length=200, blank=True, verbose_name="Fan")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'teachers'
        ordering = ['first_name', 'last_name']
        verbose_name = "O'qituvchi"
        verbose_name_plural = "O'qituvchilar"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"



@receiver(post_save, sender=Organization)
def create_organization_settings(sender, instance, created, **kwargs):
    """Auto-create OrganizationSettings when Organization is created"""
    if created:
        OrganizationSettings.objects.create(organization=instance)
