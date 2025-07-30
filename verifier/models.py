from django.db import models
from django.contrib.auth.models import User


class VerificationResult(models.Model):
    PREDICTION_CHOICES = [
        ('True', 'True News'),
        ('Fake', 'Fake News'),
        ('Partially True', 'Partially True'),
    ]
    
    CATEGORY_CHOICES = [
        ('Politics', 'Politics'),
        ('Technology', 'Technology'),
        ('Health', 'Health'),
        ('Sports', 'Sports'),
        ('Entertainment', 'Entertainment'),
        ('Business', 'Business'),
        ('Science', 'Science'),
        ('Other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    content = models.TextField()
    prediction = models.CharField(max_length=20, choices=PREDICTION_CHOICES)
    confidence = models.FloatField(default=0.0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Other')
    created_at = models.DateTimeField(auto_now_add=True)
    is_bookmarked = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title[:50]} - {self.prediction}"
    
    @property
    def content_preview(self):
        return self.content[:100] + '...' if len(self.content) > 100 else self.content


class TrendingTopic(models.Model):
    topic = models.CharField(max_length=200, unique=True)
    verification_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-verification_count', '-updated_at']
    
    def __str__(self):
        return f"{self.topic} - {self.verification_count} checks"
