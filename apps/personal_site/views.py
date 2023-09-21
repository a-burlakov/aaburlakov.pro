from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from rest_framework import generics

from .models import Article, ArticleTags, ArticleImages
from .serializers import ArticleSerializer


def header_data() -> dict:
    return {
        'page_title': 'Алексей Бурлаков | Python-разработчик',
        'title_name': 'Алексей Бурлаков',
        'subtitle_span': 'Python',
        'subtitle_text': '-разработчик',
        'email': 'fln@mail.ru',
        'telegram': 'https://t.me/aaburlakov',
        'vk': 'https://vk.com/a_a_burlakov',
        'github': 'https://github.com/a-burlakov',
        'linkedin': '',
        'resume': 'https://aaburlakov.ru/media/resume.pdf',  # deeply sorry for that, but I'm not Django user anymore
    }


def aaburlakov(request):
    """
    View to show full one-page site.
    """
    recent_posts = (
        Article.objects.filter(archived=False, article_type='BL', access_by_link=False)
        .order_by('-date')
        .only('title', 'date', 'slug', 'text')[:5]
    )

    tags = ArticleTags.objects.filter(archived=False)

    content = {
        'recent_posts': recent_posts,
        'tags': tags,
    } | header_data()
    return render(request, 'personal_site/index.html', content)


class ArticleDetail(DetailView):
    """
    View to show a specific article.
    """

    model = Article
    template_name = 'personal_site/article_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.object.title
        return context


class RecentArticlesAPIView(generics.ListAPIView):
    queryset = Article.objects.filter(
        archived=False, article_type='BL', access_by_link=False
    ).order_by('-date')[:5]

    serializer_class = ArticleSerializer
