"""
WSGI config for aaburlakov_pro project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

# WSGI - это Web Server Gateway Interface. Это стандарт взаимодействия между
# программой на Python (Django в нашем случае) и веб-сервером (Apache, Nginx...)

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aaburlakov_pro.settings")

application = get_wsgi_application()
