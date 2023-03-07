import string

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from markdown import markdown

from aaburlakov_pro import settings


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

    @staticmethod
    def url_for_standard_thumbnail_image() -> str:
        """
        Returns url for image that can be put to article thumbnail.
        """
        return settings.STATIC_URL + "img/standard-thumbnail-image.png"

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
        templates to be provided to HTML class for filtering posts
        (e.g. "article_list.html" template).
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
