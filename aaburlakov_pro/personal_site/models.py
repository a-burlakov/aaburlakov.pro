from django.db import models
from django.utils.translation import gettext_lazy as _  # from documentation


# Одно из не сразу очевидных преимуществ использования ORM - это
# возможность использовать одно и то же приложение с ORM для любых БД,
# которые поддерживаются ORM.


class Women(models.Model):
    """
    Женщины (спасибо selfedu за интересные уроки).
    """
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")

    # Новые для меня параметры "auto_now_add" и "auto_now".
    # Первый - устанавливает в поле текущее время в момент первой записи.
    # Второй - устанавливает в поле текущее время каждый раз при изменении.
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    is_published = models.BooleanField(default=True)


class Article(models.Model):
    """
    Article for site blog or resume block.
    """
    title = models.CharField("Название", max_length=250)
    sub_title = models.CharField("Подзаголовок", max_length=250, blank=True)
    image = models.ImageField("Главное изображение",
                              upload_to="article_images/")
    text = models.TextField("Текст")
    date = models.DateTimeField("Дата", auto_now_add=True)
    archived = models.BooleanField("Архив")
    slug = models.SlugField("URL-путь", max_length=80, null=True)

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

    def is_blog_post(self):
        return self.article_type == self.ArticleTypes.BLOG

    def is_project_post(self):
        return self.article_type == self.ArticleTypes.PROJECT

    class Meta:
        ordering = ["-date"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
