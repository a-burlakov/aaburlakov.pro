from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _  # from documentation


# https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/
# All database fields
# Custom manager attributes
# class Meta
# def __str__()
# def save()
# def get_absolute_url()
# Any custom methods


# Одно из не сразу очевидных преимуществ использования ORM - это
# возможность использовать одно и то же приложение с ORM для любых БД,
# которые поддерживаются ORM.

# У каждой модели есть свой объект "objects", оторый представлет собой ссылку
# на специальный класс Manager. С помощью него можно обращаться к БД:
# создавать новые записи, или собирать их по условиям.
# Women.objects.all() возвратит нам QuerySet. В нем можно обращаться по индексу
# к конкретному экземпляру. Можно циклом по ним ходить и т.д.

# Чтобы выбрать объекты по типу, нужно использовать
# Women.objects.filter(title = "Энн Хэтэуэй")
# Есть ещё метод exclude. Women.objects.exclude(title = "Энн Хэтэуэй")

# Для полей есть еще служебные поля с постфиксами __gte и __lte.
# Например Women.objects.filter(pk__gte=2) даст записи с pk большим или равным
# 2.

# Если мы хотим выбрать одну-единственную запись, надо использовать не filter,
# а get(). Например, Women.objects.get(pk=3).
# Он будет вызывать исключения, если объектов возвратится больше 1 или 0.


# Если мы хотим еще и сортировку, то нужно использовать order_by().
# Например, Women.objects.filter(pk__lte=4).order_by('title'). В общем, это
# метод queryset.
#
# Методы filter, order_by и другие можно использовать цепочкой. С ними будет
# формироваться SQL-запроса.
from aaburlakov_pro import settings


class Women(models.Model):
    """
    Женщины (спасибо selfedu за интересные уроки).
    """

    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    time_create = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField("URL-путь", unique=True, max_length=100, db_index=True)
    # Новые для меня параметры "auto_now_add" и "auto_now".
    # Первый - устанавливает в поле текущее время в момент первой записи.
    # Второй - устанавливает в поле текущее время каждый раз при изменении.
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = "Известные женщины"
        verbose_name_plural = "Известные женщины"
        ordering = ["time_create", "title"]

    def __str__(self):
        return self.title

    # Функция reverse формирует URL с таким же адресом, как указан в
    # первом параметре.
    # get_absolute_url - принятое имя для модели, его можно использовать легко
    def get_absolute_url(self):
        return reverse("post_women", kwargs={"post_id": self.pk})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_id": self.pk})


class ArticleTypes(models.TextChoices):
    """
    Types for articles. Used as enumeration for Article model.
    """

    BLOG = "BL", _("Blog post")
    PROJECT = "PR", _("Project post")


class Article(models.Model):
    """
    Article for site blog or resume block.
    """

    title = models.CharField("Название", max_length=250)
    sub_title = models.CharField("Подзаголовок", max_length=250, blank=True)
    date = models.DateField("Дата", null=True, blank=True)
    text = models.TextField("Текст")
    tags = models.ManyToManyField("ArticleTags", verbose_name="Тэги")
    image = models.ImageField(
        "Главное изображение", upload_to="article_images/", blank=True
    )
    slug = models.SlugField(
        "Путь URL", max_length=80, null=True, unique=True, db_index=True
    )
    article_type = models.CharField(
        "Тип", max_length=2, choices=ArticleTypes.choices, default=ArticleTypes.BLOG
    )
    archived = models.BooleanField("Архив")

    class Meta:
        ordering = ["-date"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.title

    def save(self):
        if not self.date:
            self.date = timezone.now()
        super(Article, self).save()

    def get_absolute_url(self) -> str:
        """
        Returns absolute URL for an article.
        """
        return reverse("blog", kwargs={"slug": self.slug})

    def is_blog_post(self) -> bool:
        return self.article_type == ArticleTypes.BLOG

    def is_project_post(self) -> bool:
        return self.article_type == ArticleTypes.PROJECT

    def tags_line(self) -> str:
        """
        Returns line of tags separated by spaces. This line is need in some
        templates to be provided to HTML class for filtering posts.
        """
        tags = list(self.tags.all())
        return " ".join([x.name for x in tags])

    def time_to_read(self) -> str:
        """
        Returns a string of information about how long it takes to read
        a post based on it's body length.
        """

        # Let's set that medium person reads ~1500 symbols a minute.
        symbols_per_minute = 1500
        body_length = len(self.text)

        if body_length < symbols_per_minute / 2:
            time_to_read = "менее минуты на чтение"
        elif body_length < symbols_per_minute:
            time_to_read = "минута на чтение"
        else:
            minutes_to_read = (body_length // symbols_per_minute) + 1
            time_to_read = f"{minutes_to_read} мин. на чтение"

        return time_to_read

    def image_path(self) -> str:
        """
        Returns string from "image" field or standard image otherwise.
        """

        if self.image:
            image_path = self.image.url
        else:
            image_path = settings.MEDIA_URL + "article_images/blog-no-picture.png"
        return image_path


class ArticleTags(models.Model):
    """
    Tags for article. Used to filter articles interactively.
    """

    name = models.CharField("Название", max_length=50)
    archived = models.BooleanField("Архив")

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.name
