from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

# В представление (view) попадает строка запроса вида http://127.0.0.1:8000/women/madonna/
# Представление по внутренней логике собирает информацию по Model и Templates
# Модель предоставляет данные, а Шаблон - шаблон HTML, который надо заполнить
# данными. Это и есть MTV (MVC).
# Представления в терминологии MVC - это контроллеры.
from personal_site.models import Women, Article, ArticleTags

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'}
]


def index(request):
    # Функция render всегда принимает request как первый параметр.
    # По сути render рендерит HTML на основании запроса и шаблона.
    posts = Women.objects.all()
    context = {
        "menu": menu,
        "title": "главная страница",
        "posts": posts
    }
    return render(request, "women/index.html", context=context)


def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")


def aaburlakov(request):
    """
    View to show full one-page site.
    """
    posts = Article.objects.filter(archived=False, article_type='BL').order_by('-date')
    recent_posts = posts[:5]
    tags = ArticleTags.objects.filter(archived=False)
    content = {
        'posts': posts,
        'recent_posts': recent_posts,
        'tags': tags
    }
    return render(request, "personal_site/index.html", content)


def about(request):
    return render(request, 'women/about.html',
                  {'menu': menu, 'title': 'О сайте'})


def addpage(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


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
