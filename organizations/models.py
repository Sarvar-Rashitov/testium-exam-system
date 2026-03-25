from django.db import models
from django.contrib.auth.models import AbstractUser


class Organization(AbstractUser):
    """Organization model - extends Django User for authentication"""
    organization_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'organizations'
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
    
    def __str__(self):
        return self.organization_name
