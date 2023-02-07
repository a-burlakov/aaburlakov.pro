from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _  # from documentation


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
class Women(models.Model):
    """
    Женщины (спасибо selfedu за интересные уроки).
    """

    def __str__(self):
        return self.title

    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")

    # Новые для меня параметры "auto_now_add" и "auto_now".
    # Первый - устанавливает в поле текущее время в момент первой записи.
    # Второй - устанавливает в поле текущее время каждый раз при изменении.
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    is_published = models.BooleanField(default=True)

    # Функция reverse формирует URL с таким же адресом, как указан в
    # первом параметре.
    # get_absolute_url - принятое имя для модели, его можно использовать легко
    def get_absolute_url(self):
        return reverse("post", kwargs={"post_id": self.pk})


class ArticleTags(models.Model):
    """
    Tags for article. Used to filter articles interactively.
    """

    def __str__(self):
        return self.name

    name = models.CharField("Название", max_length=50)
    archived = models.BooleanField("Архив")

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"


class Article(models.Model):
    """
    Article for site blog or resume block.
    """

    def __str__(self):
        return self.title

    title = models.CharField("Название", max_length=250)
    sub_title = models.CharField("Подзаголовок", max_length=250, blank=True)
    image = models.ImageField("Главное изображение",
                              upload_to="article_images/",
                              blank=True)

    def image_path(self) -> str:
        """
        Returns string from "image" field of standard image otherwise.
        """
        image_path = self.image
        if not image_path:
            image_path = 'article_images/blog-no-picture.png'
        return image_path

    text = models.TextField("Текст")
    date = models.DateField("Дата", null=True, blank=True)
    archived = models.BooleanField("Архив")
    slug = models.SlugField("Путь URL", max_length=80, null=True)

    class ArticleTypes(models.TextChoices):
        """
        Types for articles.
        """
        BLOG = 'BL', _("Blog post")
        PROJECT = 'PR', _("Project post")

    article_type = models.CharField("Тип",
                                    max_length=2,
                                    choices=ArticleTypes.choices,
                                    default=ArticleTypes.BLOG)

    tags = models.ManyToManyField(ArticleTags, verbose_name="Тэги")

    def is_blog_post(self) -> bool:
        return self.article_type == self.ArticleTypes.BLOG

    def is_project_post(self) -> bool:
        return self.article_type == self.ArticleTypes.PROJECT

    def time_to_read(self) -> str:
        """
        Returns a string of information about how long it takes to read
        a post based on it's body length.
        """

        # Let's set that medium person reads ~1500 symbols a minute.
        symbols_per_minute = 1500
        body_length = len(self.text)

        if body_length < symbols_per_minute / 2:
            time_to_read = 'менее минуты на чтение'
        elif body_length < symbols_per_minute:
            time_to_read = 'минута на чтение'
        else:
            minutes_to_read = (body_length // symbols_per_minute) + 1
            time_to_read = f'{minutes_to_read} мин. на чтение'

        return time_to_read

    def get_absolute_url(self) -> str:
        """
        Returns absolute URL for an article.
        """
        return reverse("blog", kwargs={"slug": self.slug})

    def save(self):
        if not self.date:
            self.date = timezone.now()
        super(Article, self).save()

    class Meta:
        ordering = ["-date"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
