from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path("", WomenHome.as_view(), name="home"),
    path("aaburlakov/", cache_page(60)(aaburlakov), name="aaburlakov"),
    path(
        "aaburlakov/blog/<slug:slug>/",
        ArticleDetail.as_view(),
        name="article_detail",
    ),
    path("about/", about, name="about"),
    path("addpage/", addpage, name="add_page"),
    path("contact/", contact, name="contact"),
    path("login/", login, name="login"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("post_women/<int:post_id>/", show_post, name="post_women"),
    path("category/<slug:cat_slug>/", WomenCategory.as_view(), name="category"),
]
