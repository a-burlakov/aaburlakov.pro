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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from aaburlakov_pro import settings
from personal_site.views import *

# В этом файле мы связываем url, которые ввел пользователь, с views из наших
# приложений.

urlpatterns = [
    # path("", index), # http://127.0.0.1:8000/
    path("admin/", admin.site.urls),
    # В url можно помещать параметры. Они вот каких типов они могут быть:
    # str, int, slug, uuid, path
    # path - вообще любая строка
    # str исключает только символ /
    # slug (переводится как "шлюз", а не "слизняк") - символы для URL, то есть ascii, дефис и подчеркивание
    # uuid - символы для идентификаторов, то есть дефис и ascii
    path("cats/<int:cat_id>/", categories),  # http://127.0.0.1:8000/cats/
    # В URL можно поместить даже обработку регулярных выражений через "re_path()"
    re_path(r"^archive/(?P<year>[0-9]{4})/", archive),
    # Правильная практика - обращаться через include. Все те пути, которые мы назначим
    # в файле "personal_site.urls", будут начинаться с корневого http://127.0.0.1:8000/personal_site/
    # "personal_site" мы как раз здесь и указали в первом параметре.
    # То есть методом include мы как бы включаем (include же, ну) вместе все
    # пути из "personal_site.urls" для этого пути. Пишу это, потому что
    # не сразу понял, как include этот запомнить.
    # # path("personal_site/", include('personal_site.urls')),
    # Но для своего сайта я сделаю пустой путь, потому что мое приложение
    # personal_site - оно по умолчанию.
    path("", include("personal_site.urls")),
    # Параметр name - очень важная вещь. Она позволяет закрепить за именем
    # этот путь, чтобы не хардкодить его по всему проекту, если мы будем на
    # него ссылаться. Например, извне можно написать 'return redirect("home")',
    # и Django поймет, что нужно перенаправить на этот путь
    # path("", index, name="home"),
    path("silk/", include("silk.urls", namespace="silk")),
    path("api/v1/womenlist/", WomenAPIList.as_view()),
    path("api/v1/womenlist/<int:pk>/", WomenAPIUpdate.as_view()),
    path("api/v1/womendetail/<int:pk>/", WomenAPIDetailView.as_view()),
    path("api/v1/recentarticles/", RecentArticlesAPIView.as_view()),
]

# На отладочном веб-сервере необходимо сэмулировать работу настоящего сервера
# для получения ранее загруженных файлов нашему приложению. Для этого пишем
# такую строчку.
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# В этом модуле можно прописывать переменные handlerXXX для обработки кодов
# ошибок. Этим переменным назначаются классы view, которые необходмо вызывать
# в таких случаях.
# Будет работать, только если DEBUG = False
handler404 = pageNotFound
