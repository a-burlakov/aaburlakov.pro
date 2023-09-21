from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    path = serializers.SlugField(source='get_absolute_url')

    class Meta:
        model = Article
        fields = ('title', 'sub_title', 'date', 'path')
