
from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('contacts/', None),
    path('about_me/', None),
    path('resume/', None),
]