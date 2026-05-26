from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

# Custom user model used across the app for profile fields and authentication.
class MyUser(AbstractUser):
    homepage = models.URLField(null=True, blank=True)
    display_name = models.CharField(max_length=40, null=True, blank=True)
    age = models.IntegerField(default=115)

    def __str__(self):
        return self.username

class MyTicket(models.Model):
    NEW = 'N'
    IN_PROGRESS = 'P'
    DONE = 'D'
    INVALID = 'I'
    STATUS_CHOICES = [
        (NEW, 'New'),
        (IN_PROGRESS, 'In Progress'),
        (DONE, 'Done'),
        (INVALID, 'Invalid'),
    ]

    title = models.CharField(max_length=20)
    date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=200)
    status = models.CharField(
        max_length=1,
        # Only a short code is stored; labels are presented in the UI.
        choices=STATUS_CHOICES,
        default=NEW,
    )
    # Creator is required and used to enforce edit/delete permissions.
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', on_delete=models.CASCADE)
    # Optional assignee for the ticket workflow.
    user_assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', on_delete=models.CASCADE, null=True)
    # Optional completion owner to track who closed the ticket.
    user_who_completed = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['status']

    def __str__(self):
        return self.title