from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

# В представление (view) попадает строка запроса вида http://127.0.0.1:8000/women/madonna/
# Представление по внутренней логике собирает информацию по Model и Templates
# Модель предоставляет данные, а Шаблон - шаблон HTML, который надо заполнить
# данными. Это и есть MTV (MVC).
# Представления в терминологии MVC - это контроллеры.
from django.views.generic import ListView, DetailView

from personal_site.forms import AddPostForm
from personal_site.models import Women, Article, ArticleTags

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


class WomenHome(ListView):
    model = Women
    template_name = "women/index.html"

    # Чтобы в классах представлений назначать данные, необходимо
    # использовать вот такую функцию "get_context_data()".
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        context["menu"] = menu
        context["cat_selected"] = 0
        return context

    # Здесь, через эту функцию, можно определит, какой запрос будет использоваться
    # для модели в этой вьюшке.
    def get_queryset(self):
        return Women.objects.filter(is_published=True)


# def index(request):
#     # Функция render всегда принимает request как первый параметр.
#     # По сути render рендерит HTML на основании запроса и шаблона.
#     posts = Women.objects.all()
#     context = {
#         "menu": menu,
#         "title": "Главная страница",
#         "posts": posts,
#         "cat_selected": 0,
#     }
#     return render(request, "women/index.html", context=context)


def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")


class WomenCategory(ListView):
    model = Women
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False  # Генерирует404 статей нет

    def get_queryset(self):
        return Women.objects.filter(
            cat__slug=self.kwargs["cat_slug"], is_published=True
        )


# def show_category(request, cat_id):
#     posts = Women.objects.filter(cat=cat_id)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         "menu": menu,
#         "title": "По рубрикам",
#         "posts": posts,
#         "cat_selected": cat_id,
#     }
#     return render(request, "women/index.html", context=context)


def aaburlakov(request):
    """
    View to show full one-page site.
    """
    posts = Article.objects.filter(archived=False, article_type="BL").order_by("-date")
    projects = Article.objects.filter(archived=False, article_type="PR").order_by(
        "-date"
    )
    recent_posts = posts[:5]
    tags = ArticleTags.objects.filter(archived=False)
    content = {
        "posts": posts,
        "projects": projects,
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


def about(request):
    return render(request, "women/about.html", {"menu": menu, "title": "О сайте"})


def addpage(request):
    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            # Women.objects.create(**form.cleaned_data)
            form.save()  # команда сохраняет элемент, если модель связана с формой
            return redirect("home")
    else:
        form = AddPostForm()

    return render(
        request,
        "women/addpage.html",
        {"menu": menu, "form": form, "title": "Добавление статьи"},
    )


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
        return redirect("home", permanent=True)  # Происходит код 301 - постоянный

    return HttpResponse(f"<h1>Год из регулярок:</h1><p>{year}</p>")


def pageNotFound(request, exception):
    # HttpResponseNotFound возвращает код 404, этим отличается от HttpResponse
    # параметр exception здесь - это первый параметр в raise Http404('test')
    return HttpResponseNotFound("Страница не найдена!!!")
