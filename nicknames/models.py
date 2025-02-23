from django.db import models
from django.contrib.auth.models import User

class Nickname(models.Model):
    given_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_nicknames')
    given_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_nicknames')
    nickname = models.CharField(max_length=100)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['given_to', 'given_by']

class Reaction(models.Model):
    REACTION_CHOICES = [
        ('LIKE', '👍'),
        ('LOVE', '❤️'),
        ('LAUGH', '😂'),
        ('WOW', '😮'),
    ]
    
    nickname = models.ForeignKey(Nickname, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    
    class Meta:
        unique_together = ['nickname', 'user']

class Report(models.Model):
    REPORT_REASONS = [
        ('OFFENSIVE', 'Offensive Content'),
        ('HARASSMENT', 'Harassment'),
        ('INAPPROPRIATE', 'Inappropriate Content'),
        ('SPAM', 'Spam'),
        ('OTHER', 'Other')
    ]
    
    nickname = models.ForeignKey(Nickname, on_delete=models.CASCADE, related_name='reports')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['nickname', 'reported_by'] 