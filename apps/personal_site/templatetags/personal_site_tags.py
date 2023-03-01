from django import template
from django.db.models import Prefetch

from apps.personal_site.models import Article, ArticleImages, ArticleTags

register = template.Library()


@register.inclusion_tag("personal_site/inclusion_tags/article_list.html")
def article_list(article_type: str):
    """
    Tag to show articles list at site depending on article type.
    """
    articles = (
        Article.objects.filter(archived=False, article_type=article_type)
        .prefetch_related(
            Prefetch(
                "images",
                queryset=ArticleImages.objects.filter(default=True).only("image"),
            ),
        )
        .prefetch_related(
            Prefetch("tags", queryset=ArticleTags.objects.filter(archived=False))
        )
        .order_by("-date")
    )

    for article in articles:
        article.tags_line = article.tags_line()
        article.tags_line_for_html = article.tags_line_for_html()
        default_images = article.images.all()
        if default_images:
            article.default_image_path = default_images[0].image.url
        else:
            article.default_image_path = article.url_for_standard_thumbnail_image()

    if article_type == "PR":
        tags = []
        section_id = "projects"
    else:
        tags = ArticleTags.objects.filter(archived=False)
        section_id = "blog"

    return {
        "articles": articles,
        "tags": tags,
        "section_id": section_id,
    }
