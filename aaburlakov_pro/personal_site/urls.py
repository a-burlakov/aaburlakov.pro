
from django.urls import path
from .views import *

urlpatterns = [
    path("", index),
    path("aa/", aaburlakov, name="aaburlakov"),
    path("about/", about, name="about")
    # path('blog/<slug:slug>/', index),
    # path('contacts/', None),
    # path('about_me/', None),
    # path('resume/', None),
    # path('courses/', None),
]


