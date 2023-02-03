from django.http import HttpResponse
from django.shortcuts import render

# В представление (view) попадает строка запроса вида http://127.0.0.1:8000/women/madonna/
# Представление по внутренней логике собирает информацию по Model и Templates
# Модель предоставляет данные, а Шаблон - шаблон HTML, который надо заполнить
# данными. Это и есть MTV (MVC).
# Представления в терминологии MVC - это контроллеры.


def index(request):
    return HttpResponse("Страница приложения personal_site")


def categories(request):
    return HttpResponse("<h1>ЧТО ПРОиЗхОдИт</h1>")