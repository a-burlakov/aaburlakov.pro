"""aaburlakov_pro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from personal_site.views import index, categories

# В этом файле мы связываем url, которые ввел пользователь, с views из наших
# приложений.

urlpatterns = [
    # path("", index), # http://127.0.0.1:8000/
    path("admin/", admin.site.urls),
    path("cats/", categories), # http://127.0.0.1:8000/cats/

    # Правильная практика - обращаться через include. Все те пути, которые мы назначим
    # в файле "personal_site.urls", будут начинаться с корневого http://127.0.0.1:8000/personal_site/
    # "personal_site" мы как раз здесь и указали в первом параметре.
    # То есть методом include мы как бы включаем (include же, ну) вместе все
    # пути из "personal_site.urls" для этого пути. Пишу это, потому что
    # не сразу понял, как include этот запомнить.
    # # path("personal_site/", include('personal_site.urls')),

    # Но для своего сайта я сделаю пустой путь, потому что мое приложение
    # personal_site - оно по умолчанию.
    path("", include("personal_site.urls"))
]
