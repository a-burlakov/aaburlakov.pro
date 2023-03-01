from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    # TODO: вернуть кэш
    # path("", cache_page(60 * 15)(aaburlakov), name="home"),
    path("", (aaburlakov)),
    path(
        "blog/<slug:slug>/",
        # cache_page(60 * 15)(ArticleDetail.as_view()),
        (ArticleDetail.as_view()),
        name="article_detail",
    ),
    path("api/v1/recentarticles/", RecentArticlesAPIView.as_view()),
]
