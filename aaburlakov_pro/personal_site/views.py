from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from rest_framework import generics

from personal_site.models import Article, ArticleTags, ArticleImages
from personal_site.serializers import ArticleSerializer


def aaburlakov(request):
    """
    View to show full one-page site.
    """
    recent_posts = (
        Article.objects.filter(archived=False, article_type="BL")
        .order_by("-date")
        .only("title", "date", "slug", "text")[:5]
    )
    tags = ArticleTags.objects.filter(archived=False)
    content = {
        "recent_posts": recent_posts,
        "tags": tags,
    }
    return render(request, "personal_site/index.html", content)


class ArticleDetail(DetailView):
    """
    View to show a specific article.
    """

    model = Article
    template_name = "personal_site/article_detail.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RecentArticlesAPIView(generics.ListAPIView):
    queryset = Article.objects.filter(archived=False, article_type="BL").order_by(
        "-date"
    )[:5]

    serializer_class = ArticleSerializer
