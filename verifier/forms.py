from django import forms
from .models import VerificationResult


class NewsVerificationForm(forms.Form):
    title = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter news headline (optional)',
            'rows': 1
        }),
        label='News Headline'
    )
    
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Paste the full article text or headline here...',
            'rows': 8
        }),
        label='Article Content',
        help_text='Paste the news content you want to verify for authenticity.'
    )
    
    category = forms.ChoiceField(
        choices=VerificationResult.CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Category (Optional)'
    )
    
    save_to_history = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Save to my verification history'
    )


class HistoryFilterForm(forms.Form):
    RESULT_CHOICES = [
        ('', 'All Results'),
        ('True', 'True News'),
        ('Fake', 'Fake News'),
        ('Partially True', 'Partially True'),
    ]
    
    result_filter = forms.ChoiceField(
        choices=RESULT_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Filter by Result'
    )
    
    category_filter = forms.ChoiceField(
        choices=[('', 'All Categories')] + VerificationResult.CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Filter by Category'
    )
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search in titles and content...'
        }),
        label='Search'
    )
