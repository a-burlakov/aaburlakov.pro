# Тэги должны располагаться в каталоге templatetags, и в нем должен быть
# файл __init.py.

from django import template

from personal_site.models import *

# Через Library происходит регистрация шаблонных тэгов.
register = template.Library()


# Простые теги - это, по сути функции, которе можно определить здесь, в
# templatetags, и через декоратор регистрировать их. Потом нужно загрузить
# их как {% load personal_site_tags %} в шаблоне, и вызывать.
@register.simple_tag(name="getcats")
def get_categories():
    return Category.objects.all()


# Есть еще включающие теги. Они, в отличие от простых тегов, возвращают не
# просто коллекцию, но еще и html. Могут быть параметризируемые.
@register.inclusion_tag("women/list_categories.html")
def show_categories():
    # Здесь мы определяем коллекцию cats, и через декоратор определяем, что
    # этот тэг будет возвращать html в который уже переданы параметры, если
    # в него передать параметр cats.
    # Обычно такие служебные html помещают в отдельную папку.
    cats = Category.objects.all()
    return {"cats": cats}


@register.inclusion_tag("personal_site/inclusion_tags/article_list.html")
def article_list(article_type: str):
    """
    Tag to show articles list at site separated by types.
    """
    articles = Article.objects.filter(
        archived=False, article_type=article_type
    ).order_by("-date")

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
