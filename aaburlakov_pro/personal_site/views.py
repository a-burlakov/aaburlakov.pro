from django.contrib.auth.forms import UserCreationForm
from django.db.models import Prefetch
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import generics

# В представление (view) попадает строка запроса вида http://127.0.0.1:8000/women/madonna/
# Представление по внутренней логике собирает информацию по Model и Templates
# Модель предоставляет данные, а Шаблон - шаблон HTML, который надо заполнить
# данными. Это и есть MTV (MVC).
# Представления в терминологии MVC - это контроллеры.
from django.views.generic import ListView, DetailView, CreateView
from rest_framework.response import Response
from rest_framework.views import APIView
from silk.profiling.profiler import silk_profile

from personal_site.forms import AddPostForm
from personal_site.models import Women, Article, ArticleTags, Category, ArticleImages
from personal_site.serializers import WomenSerializer, ArticleSerializer


class WomenAPIList(generics.ListCreateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer


class WomenAPIUpdate(generics.UpdateAPIView):
    # Пусть queryset у нас берет all, все равно из-за наследованной
    # вьюшки мы возвратим только единственную запись. Она возвратится,
    # потому что кверисеты ленивые, и остановятся на первой записи
    # (как-то так)
    queryset = Women.objects.all()
    serializer_class = WomenSerializer


# Эта вьюшка умеет делать вообще весь CRUD, вау.
class WomenAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer


# class WomenAPIView(APIView):
#     def get(self, request):
#         w = Women.objects.all().values()
#         # параметр "many" говорит о том, что сериализатору нужно
#         # выдавать не одну запись, а много
#         return Response(
#             {"posts": WomenSerializer(w, many=True).data},
#         )
#
#     def post(self, request):
#         serializer = WomenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({"post": serializer.data})
#
#     # Метод PUT служит для изменения или вставки ресурса. В требовании изменения
#     # должен быть задан уникальный ID указанного ресурса.
#     def put(self, request, *args, **kwargs):
#         # в PUT мы изменяем объет. Предполагается, что pk мы передаем.
#         # здесь ищем этот pk
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method PUT not allowed"})
#
#         # по PK ищем наш объект.
#         try:
#             instance = Women.objects.get(pk=pk)
#         except:
#             return Response({"error": "Object does not exist"})
#
#         # когда нашли, по помещаем в сериализатор данные из запроса,
#         # проверяем и передаем, что все ок.
#         serializer = WomenSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"post": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method DELETE not allowed"})
#
#         try:
#             instance = Women.objects.get(pk=pk)
#             instance.delete()
#         except:
#             return Response({"error": "Object could not be deleted"})
#
#         return Response({"post": "delete post " + str(pk)})


# class WomenAPIView(generics.ListAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer


class ArticleAPIView(generics.ListAPIView):
    queryset = Article.objects.filter(archived=False)
    serializer_class = ArticleSerializer


class RecentArticlesAPIView(generics.ListAPIView):
    queryset = Article.objects.filter(archived=False, article_type="BL").order_by(
        "-date"
    )

    serializer_class = ArticleSerializer


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
    recent_posts = (
        Article.objects.filter(archived=False, article_type="BL")
        .order_by("-date")
        .only("title", "date", "slug", "text")[:5]
    )
    tags = ArticleTags.objects.filter(archived=False)
    content = {
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


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.all()
        context["menu"] = menu
        context["cats"] = cats
        if "cat_selected" not in context:
            context["cat_selected"] = 0
        return context


class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = "women/register.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))


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
