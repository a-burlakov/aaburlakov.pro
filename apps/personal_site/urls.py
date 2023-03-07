from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *


urlpatterns = [
    path("", (aaburlakov), name="home"),
    path(
        "blog/<slug:slug>/",
        (ArticleDetail.as_view()),
        name="article_detail",
    ),
    path("api/v1/recentarticles/", RecentArticlesAPIView.as_view()),
]
