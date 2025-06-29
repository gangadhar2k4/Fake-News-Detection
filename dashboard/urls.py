from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/stats/', views.user_stats_api, name='user_stats_api'),
]
