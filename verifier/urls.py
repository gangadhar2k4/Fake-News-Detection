from django.urls import path
from . import views

app_name = 'verifier'

urlpatterns = [
    path('', views.verify_news, name='verify'),
    path('history/', views.verification_history, name='history'),
    path('bookmark/<int:result_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('delete/<int:result_id>/', views.delete_result, name='delete_result'),
    path('grok-setup/', views.grok_setup, name='grok_setup'),
]
