from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from verifier.models import VerificationResult, TrendingTopic
from verifier.views import get_trending_topics
from datetime import datetime, timedelta


@login_required
def dashboard(request):
    """Main dashboard view with user statistics"""
    user = request.user
    
    # Get user statistics
    total_checks = VerificationResult.objects.filter(user=user).count()
    true_news_count = VerificationResult.objects.filter(user=user, prediction='True').count()
    fake_news_count = VerificationResult.objects.filter(user=user, prediction='Fake').count()
    partially_true_count = VerificationResult.objects.filter(user=user, prediction='Partially True').count()
    bookmarked_count = VerificationResult.objects.filter(user=user, is_bookmarked=True).count()
    
    recent_checks = VerificationResult.objects.filter(user=user)[:5]
    
    trending_topics = get_trending_topics()
    
    week_ago = datetime.now() - timedelta(days=7)
    weekly_checks = VerificationResult.objects.filter(
        user=user,
        created_at__gte=week_ago
    ).count()
    
    # Category breakdown
    category_stats = VerificationResult.objects.filter(user=user).values('category').annotate(
        count=Count('category')
    ).order_by('-count')[:5]
    
    # Monthly trend data for charts (last 6 months)
    monthly_data = []
    for i in range(6):
        month_start = datetime.now().replace(day=1) - timedelta(days=30*i)
        month_end = month_start + timedelta(days=31)
        
        month_checks = VerificationResult.objects.filter(
            user=user,
            created_at__gte=month_start,
            created_at__lt=month_end
        ).count()
        
        monthly_data.append({
            'month': month_start.strftime('%b %Y'),
            'checks': month_checks
        })
    
    monthly_data.reverse()  # Show chronological order
    
    # Accuracy insights (this week vs last week)
    last_week_start = week_ago - timedelta(days=7)
    this_week_true = VerificationResult.objects.filter(
        user=user,
        created_at__gte=week_ago,
        prediction='True'
    ).count()
    
    last_week_true = VerificationResult.objects.filter(
        user=user,
        created_at__gte=last_week_start,
        created_at__lt=week_ago,
        prediction='True'
    ).count()
    
    context = {
        'user': user,
        'total_checks': total_checks,
        'true_news_count': true_news_count,
        'fake_news_count': fake_news_count,
        'partially_true_count': partially_true_count,
        'bookmarked_count': bookmarked_count,
        'recent_checks': recent_checks,
        'trending_topics': trending_topics,
        'weekly_checks': weekly_checks,
        'category_stats': category_stats,
        'monthly_data': monthly_data,
        'this_week_true': this_week_true,
        'last_week_true': last_week_true,
    }
    
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def user_stats_api(request):
    """API endpoint for dashboard statistics (for AJAX updates)"""
    from django.http import JsonResponse
    
    user = request.user
    
    stats = {
        'total_checks': VerificationResult.objects.filter(user=user).count(),
        'true_news': VerificationResult.objects.filter(user=user, prediction='True').count(),
        'fake_news': VerificationResult.objects.filter(user=user, prediction='Fake').count(),
        'partially_true': VerificationResult.objects.filter(user=user, prediction='Partially True').count(),
        'bookmarked': VerificationResult.objects.filter(user=user, is_bookmarked=True).count(),
    }
    
    return JsonResponse(stats)
