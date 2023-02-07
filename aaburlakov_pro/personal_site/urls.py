
from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="home"),
    path("aa/", aaburlakov, name="aaburlakov"),
    path("about/", about, name="about"),
    path("addpage/", addpage, name="add_page"),
    path("contact/", contact, name="contact"),
    path("login/", login, name="login"),
    path("post_women/<int:post_id>/", show_post, name="post_women"),
    path("blog/<slug:slug>/", show_post, name="blog"),
]


