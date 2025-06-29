from django.contrib import admin
from .models import VerificationResult, TrendingTopic


@admin.register(VerificationResult)
class VerificationResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'title_preview', 'prediction', 'confidence', 'created_at')
    list_filter = ('prediction', 'created_at', 'category')
    search_fields = ('title', 'content', 'user__username')
    readonly_fields = ('created_at',)
    
    def title_preview(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    title_preview.short_description = 'Title'


@admin.register(TrendingTopic)
class TrendingTopicAdmin(admin.ModelAdmin):
    list_display = ('topic', 'verification_count', 'created_at')
    search_fields = ('topic',)
    readonly_fields = ('created_at',)
