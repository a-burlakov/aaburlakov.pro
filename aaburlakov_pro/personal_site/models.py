import string

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _  # from documentation
from markdown import markdown

from aaburlakov_pro import settings


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
# Здесь будет целая лекция по Django ORM: https://www.youtube.com/watch?v=QrO-YgfWAOU&list=PLA0M1Bcd0w8xO_39zZll2u1lz_Q-Mwn1F&index=16&ab_channel=selfedu
# - важно знать, что слайсы после queryset ограничивают не уже выполненный запрос,
# а превращаются неявно в операторы OFFSET и LIMIT на SQL, поэтому их можно использовать
# без страха.
# .reverse() - это обратный порядок. Нужно иметь в виду вместо order_by.
# - для того, чтобы выбрать один-единственный элемент, то нужно использовать .objects.get(pk=3).
# Он возвратит немного элементов, а только один.
#
# У любой модели создается специальное свойство "<имявторичной модели>_set".
# Мы можем выбрать "c" как "Category.objects.get(pk=2)"
# потом, когда мы напишем "c.women_set.all()" - мы получим женщин этой категории.
# У нас будет запрос вида "SELECT поля женщин WHERE cat_id женщины = категория "C" ".
#
# Есть ещё т.н. lookups, которые
# Если мы хотим еще и ииыв сортировку, то нужно использовать order_by().
# Например, Women.objects.filter(pk__lte=4).order_by('title'). В общем, это
# метод queryset.
#
# Вот этот класс можно использовать, если необходимо через ORM делать сложные условия
# по И или ИЛИ или НЕ.
# from django.db.models import Q
#
# Если в таблице есть поля, которые хранят дату и время, То для них можно делать
# методы earliest("поле даты") и latest. Вот так-то.
#
# Ещё прикольная штука: мы можем через ORM get получить объект a, например.
# Потом можем использовать a.get_next_by_time_update - эта штука строит запрос по
# полю time_update и выбирает следующую запись. Взрыв мозга, очень круто. Но и медленно,
# наверное.
# Также, тут можно и указать условие. Например, a.get_next_by_time_update(pl__gt=10)
#
# Полезны методы exists() и count(). Они быстрые и часто используются.
# category_object.women_set.exists() может возвратить false или true
# category_object.women_set.count() может возвратить 533 или 0
#
# Аггрегирующие функции можно использовать вот так:
# Women.objects.aggregate(Min('cat_id))
# Возвратит циферку.
# Но чтобы пользоваться ими, нужно использовать from django.db.models import *
# И потом уже использовать Min, Max, Sum, Avg и т.д.
#
# Для агрегации записей по группам можно использовать annotate.
# Women.objects.values('cat_id').annotate(total=Count('id'))
#
# В выборке записей ORM по умолчанию выбирает все возможные поля. Не всегда это хорошо,
# особенно в больших таблицах.
# Эту проблему решает .values. Мы можем использовать его вот так:
# Women.objects.values("title", "cat_id", "cat__name"). Запрос возвратит эти три поля.
# Также, values, возвращает словарь вместо QuerySet. Это важно.
# values_list вообще возвращает кортеж.
#
# Explain() возвращает строку плана выполнения запроса.
#
# Есть ещё внешний класс F, который используется, чтобы в блок WHERE помещать
# условия, связанные не просто со значениями, а с полями таблицы.
# Women.objects.filter(pk__gt=F('cat_id'))
#
# Кстати, сам sql-запрос сразу не выполняется. Чтобы запрос выполнился, нужно либо обратиться
# к query-set по элементу, или начать итерацию результатов.
#
# Если у уже почти-финализированного QuerySet вызывать "all()", то оне не вернет все-все
# результаты, он вернет то, что есть.
#
# Можно фигачить сразу raw-запросы. Выглядит это так:
# Women.objects.raw('SELECT * FROM women_women')
# на выходе получаем объект RawQuerySet.
# Это тоже ленивый запрос - он выполняется, когда мы к выборке обращаемся.
#
# Если хочется передать параметр в raw-запрос, можно использовать вот такую конструкцию:
# Women.objects.raw("SELECT id, title FROM women_women WHERE slug='%s'", [slug])
#
# Методы filter, order_by и другие можно использовать цепочкой. С ними будет
# формироваться SQL-запроса.
#
# В SQL есть такая вещь, как оконные функции. Они позволяют добавить к результату доп.
# колонку со значениями. Можно делать интересные вещи.
#


class Women(models.Model):
    """
    Женщины (спасибо selfedu за интересные уроки).
    """

    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", null=True, blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField("URL-путь", max_length=100, db_index=True, null=True)
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
    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=False,
        unique=True,
        db_index=True,
        verbose_name="URL",
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_slug": self.slug})


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
    tags = models.ManyToManyField(
        "ArticleTags", verbose_name="Тэги", blank=True, related_name="tags"
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

    @property
    def get_absolute_url(self) -> str:
        """
        Returns absolute URL for an article.
        """
        return reverse("article_detail", kwargs={"slug": self.slug})

    @property
    def is_blog_post(self) -> bool:
        return self.article_type == ArticleTypes.BLOG

    @property
    def is_project_post(self) -> bool:
        return self.article_type == ArticleTypes.PROJECT

    def tags_line(self) -> str:
        """
        Returns line of tags with "#" separated by spaces. This line is need
        for showing at web-site.
        """

        tags = ["#" + tag.name for tag in self.tags.all()]
        return " ".join(tags)

    def tags_line_for_html(self) -> str:
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

    def default_image_path(self) -> str:
        """
        Returns url for default image from "ArticleImages"
        or standard image if there's no images yet.
        """

        # default_image = self.images.filter(default=True).first()
        default_images = self.images.all()
        if default_images:
            image_path = default_images[0].image.url
        else:
            image_path = settings.MEDIA_URL + "article_images/blog-no-picture.png"
        return image_path

    def text_as_html(self) -> str:
        """
        Returns raw HTML from Markdown text in model.
        Additionally, transforms lines like "$image_N" to HTML image using
        paths from "ArticleImages" model.
        """

        md_text = self.text

        image_template = string.Template("![post-image]($url)")
        caption_template = string.Template(
            '<center class="post-image-caption">$caption</center>'
        )

        images = self.images.all()
        for i, image in enumerate(images, 1):
            image_line = f"$image_{i}"
            if image_line not in md_text:
                continue

            md_image = image_template.substitute(url=image.image.url)
            if image.caption:
                md_image += caption_template.substitute(caption=image.caption)

            md_text = md_text.replace(image_line, md_image)

        return markdown(md_text)


class ArticleImages(models.Model):
    """
    Images for Articles.
    """

    article = models.ForeignKey(
        "Article", on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField("Изображение", upload_to="article_images")
    caption = models.CharField("Подпись", max_length=250, blank=True, null=True)
    default = models.BooleanField("Титульное изображение")


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
