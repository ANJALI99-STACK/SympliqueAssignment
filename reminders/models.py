from django.db import models
from django.utils import timezone

class Reminder(models.Model):
    message = models.CharField(max_length=255)
    reminder_type = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    remind_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        # Ensure remind_at is timezone-aware before saving
        if hasattr(self, 'remind_at') and not timezone.is_aware(self.remind_at):
            self.remind_at = timezone.make_aware(self.remind_at)
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Reminder: {self.message} at {self.remind_at}"