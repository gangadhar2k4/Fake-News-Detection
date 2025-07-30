"""
WSGI config for fake_news_detector project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fake_news_detector.settings')

application = get_wsgi_application()
