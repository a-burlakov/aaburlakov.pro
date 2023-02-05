from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

# В представление (view) попадает строка запроса вида http://127.0.0.1:8000/women/madonna/
# Представление по внутренней логике собирает информацию по Model и Templates
# Модель предоставляет данные, а Шаблон - шаблон HTML, который надо заполнить
# данными. Это и есть MTV (MVC).
# Представления в терминологии MVC - это контроллеры.
from personal_site.models import Women

menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]


def index(request):
    # Функция render всегда принимает request как первый параметр.
    # По сути render рендерит HTML на основании запроса и шаблона.
    posts = Women.objects.all()
    return render(request, "women/index.html", {"menu": menu,
                                                "title": "главная страница",
                                                "posts": posts})


def about(request):
    return render(request, "women/about.html", {"title": "о сайте"})


def categories(request, cat_id: int):
    # Если в запросе есть параметры, например "http://127.0.0.1:8000/cats/1/?name=gagarina&type=pop",
    # то обратиться к ним можно через словари request.GET или request.POST и т.д.
    if request.POST:
        print(request.POST)

    return HttpResponse(f"<h1>ЧТО ПРОиЗхОдИт</h1><p>{cat_id}</p> ")


def archive(request, year):
    # if int(year) > 2020:
    #     raise Http404()  # По этому исключению мы сразу уходим handler404 (см. url проекта)

    # Редиректы.
    # Кстати, код 301 - это переход на постоянный URL, а 302 - на временный.
    # 301 или 302 - зависит от параметра permanent (по умолчанию False)
    if int(year) > 2020:
        return redirect("home",
                        permanent=True)  # Происходит код 301 - постоянный

    return HttpResponse(f"<h1>Год из регулярок:</h1><p>{year}</p>")


def pageNotFound(request, exception):
    # HttpResponseNotFound возвращает код 404, этим отличается от HttpResponse
    # параметр exception здесь - это первый параметр в raise Http404('test')
    return HttpResponseNotFound('Страница не найдена!!!')
