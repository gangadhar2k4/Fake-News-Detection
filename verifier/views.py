from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .forms import NewsVerificationForm, HistoryFilterForm
from .models import VerificationResult, TrendingTopic
# modified by ganga
# from .ml_utils import FakeNewsDetector
import json
from .ml_utils import APINewsVerifier

# Initialize the ML detector 
# modified
# detector = FakeNewsDetector()

detector = APINewsVerifier()

@login_required
def verify_news(request):
    """Main news verification view"""
    if request.method == 'POST':
        form = NewsVerificationForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title', '')
            content = form.cleaned_data['content']
            category = form.cleaned_data.get('category', 'Other')
            save_to_history = form.cleaned_data.get('save_to_history', True)
            
            # Use title + content for prediction, or just content if no title
            text_to_analyze = f"{title} {content}".strip() if title else content
            # Get ML prediction
            # modified
            # result = detector.predict(text_to_analyze)

            result = detector.verify_news(text_to_analyze)
            
            verification_result = None
            if save_to_history:
                verification_result = VerificationResult.objects.create(
                    user=request.user,
                    title=title or content[:100] + '...' if len(content) > 100 else content,
                    content=content,
                    prediction=result['prediction'],
                    confidence=result['confidence'],
                    category=category
                )
                update_trending_topics(category, title, content)

            context = {
                'result': result,
                'title': title,
                'content': content,
                'category': category,
                'verification_result': verification_result,
                'form': NewsVerificationForm()  
            }
            
            return render(request, 'verifier/result.html', context)
    else:
        form = NewsVerificationForm()
    
    return render(request, 'verifier/verify.html', {'form': form})


@login_required
def verification_history(request):
    """View user's verification history with filtering"""
    filter_form = HistoryFilterForm(request.GET)
    
    results = VerificationResult.objects.filter(user=request.user)
    
    if filter_form.is_valid():
        result_filter = filter_form.cleaned_data.get('result_filter')
        category_filter = filter_form.cleaned_data.get('category_filter')
        search = filter_form.cleaned_data.get('search')
        
        if result_filter:
            results = results.filter(prediction=result_filter)
        
        if category_filter:
            results = results.filter(category=category_filter)
        
        if search:
            results = results.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
    
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
        'total_results': results.count()
    }
    
    return render(request, 'verifier/history.html', context)


@login_required
def toggle_bookmark(request, result_id):
    """Toggle bookmark status of a verification result"""
    if request.method == 'POST':
        result = get_object_or_404(VerificationResult, id=result_id, user=request.user)
        result.is_bookmarked = not result.is_bookmarked
        result.save()
        
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({
                'success': True,
                'bookmarked': result.is_bookmarked
            })
        else:
            status = 'bookmarked' if result.is_bookmarked else 'removed from bookmarks'
            messages.success(request, f'Article {status} successfully.')
    
    return redirect('verifier:history')


@login_required
def delete_result(request, result_id):
    """Delete a verification result"""
    if request.method == 'POST':
        result = get_object_or_404(VerificationResult, id=result_id, user=request.user)
        result.delete()
        messages.success(request, 'Verification result deleted successfully.')
    
    return redirect('verifier:history')


def get_trending_topics():
    """Get or create trending topics"""
    topics = TrendingTopic.objects.all()[:10]
    
    if not topics.exists():
        initial_topics = [
            ('Artificial Intelligence', 1250),
            ('Climate Change', 980),
            ('Cryptocurrency', 875),
            ('Space Exploration', 750),
            ('Healthcare', 690),
            ('Politics', 650),
            ('Technology', 580),
            ('Sports', 520),
            ('Entertainment', 480),
            ('Education', 420)
        ]
        
        for topic, count in initial_topics:
            TrendingTopic.objects.get_or_create(
                topic=topic,
                defaults={'verification_count': count}
            )
        
        topics = TrendingTopic.objects.all()[:10]
    
    return topics


def update_trending_topics(category, title, content):
    """Update trending topics based on verification"""
    keywords = []
    
    if title:
        keywords.extend(title.split())
    
    if content:
        words = content.lower().split()
        important_keywords = [word for word in words 
                            if len(word) > 4 and word.isalpha()][:5]
        keywords.extend(important_keywords)
   

    category_topic, created = TrendingTopic.objects.get_or_create(
        topic=category,
        defaults={'verification_count': 1}
    )
    if not created:
        category_topic.verification_count += 1
        category_topic.save()
    
    
    for keyword in keywords[:2]: 
        if len(keyword) > 4:
            topic, created = TrendingTopic.objects.get_or_create(
                topic=keyword.title(),
                defaults={'verification_count': 1}
            )
            if not created:
                topic.verification_count += 1
                topic.save()


def grok_setup(request):
    return render(request, 'verifier/grok_setup.html')
