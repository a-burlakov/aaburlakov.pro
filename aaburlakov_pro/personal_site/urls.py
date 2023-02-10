from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="home"),
    path("aaburlakov/", aaburlakov, name="aaburlakov"),
    path("aaburlakov/blog/<slug:article_slug>/", article_detail, name="article_detail"),
    path("about/", about, name="about"),
    path("addpage/", addpage, name="add_page"),
    path("contact/", contact, name="contact"),
    path("login/", login, name="login"),
    path("post_women/<int:post_id>/", show_post, name="post_women"),
    path("category/<int:cat_id>/", show_category, name="category"),
]
