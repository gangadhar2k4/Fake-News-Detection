"""fake_news_detector URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('verifier/', include('verifier.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('',views.index,name='index'),
]
