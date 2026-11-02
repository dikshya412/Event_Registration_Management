from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student','Student'),
        ('organizer','Organizer'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )
    ONBOARDING_CHOICES = [
    ('join_events', 'Find and join events'),
    ('organize_events', 'Create and organize events'),
    ('both', 'Not sure yet - open to both'),
    ]

    onboarding_preference = models.CharField(
    max_length=20,
    choices=ONBOARDING_CHOICES,
    blank=True,
    default=''
    )
    phone = models.CharField(
        max_length=15,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    ) 

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class OrganizerRequest(models.Model):

    STATUS_CHOICES = [
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected'),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='organizer_requests'
    )
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
        )
    requested_at = models.DateTimeField(
        auto_now_add=True
    )
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.status}"
