from django.db import models
from django.core.validators import MaxLengthValidator
from django.utils import timezone
from datetime import timedelta


class Message(models.Model):
    """
    Model for storing chat messages.
    """
    username = models.CharField(max_length=50, help_text="Guest username like 'Гость-1234'")
    message_text = models.TextField(
        validators=[MaxLengthValidator(1000)],
        help_text="Message text, max 1000 characters"
    )
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Message creation timestamp")

    class Meta:
        ordering = ['timestamp']
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"{self.username}: {self.message_text[:50]}..."


class ActiveUser(models.Model):
    """
    Model for tracking online users in the chat.
    """
    session_id = models.CharField(max_length=255, unique=True, help_text="Unique session identifier")
    username = models.CharField(max_length=50, help_text="Guest username")
    last_activity = models.DateTimeField(auto_now=True, help_text="Last activity timestamp")

    class Meta:
        verbose_name = "Active User"
        verbose_name_plural = "Active Users"

    def __str__(self):
        return f"{self.username} (session: {self.session_id[:8]}...)"

    @classmethod
    def get_online_count(cls):
        """
        Returns count of users active in the last 5 minutes.
        """
        five_minutes_ago = timezone.now() - timedelta(minutes=5)
        return cls.objects.filter(last_activity__gte=five_minutes_ago).count()

    @classmethod
    def cleanup_inactive_users(cls):
        """
        Remove users inactive for more than 5 minutes.
        """
        five_minutes_ago = timezone.now() - timedelta(minutes=5)
        cls.objects.filter(last_activity__lt=five_minutes_ago).delete()
