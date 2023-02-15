from django.contrib import admin
from .models import *

# https://docs.djangoproject.com/en/4.1/ref/contrib/admin/


class WomenAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "time_create", "slug", "photo", "is_published")
    list_display_links = ("id", "title")
    search_fields = ("title", "content")


class ArticleImagesInline(admin.TabularInline):
    fk_name = "article"
    model = ArticleImages


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "article_type",
        "title",
        "sub_title",
        "slug",
        "date",
        "archived",
    )
    list_display_links = ("id", "title", "sub_title")
    search_fields = ("title", "sub_title", "text", "article_type")
    list_editable = ("slug", "archived")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        ArticleImagesInline,
    ]


class ArticleTagsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "archived")
    list_display_links = ("id", "name")
    search_fields = "name"


class ArticleImagesAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "article")
    list_display_links = "id"


# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleTags)
admin.site.register(Women, WomenAdmin)
