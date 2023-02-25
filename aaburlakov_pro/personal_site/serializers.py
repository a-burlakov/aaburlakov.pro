import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Women, Article


# class WomenModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content


class WomenSerializer(serializers.Serializer):
    # Здесь поле max_length позволяет сразу отвалидировать приходящие JSON
    # на их длину.
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    time_create = serializers.DateTimeField(read_only=True)
    time_update = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(default=True)
    cat_id = serializers.IntegerField()

    # метод, чтобы сразу через сериализатор создавать объекты
    def create(self, validated_data):
        # здесь в поля заполняются автоматом те поля, которые мы провалидировали
        return Women.objects.create(**validated_data)

    # Этот метод как раз не создает, а изменяет уже имеющийся объект.
    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.time_update = validated_data.get("time_update", instance.time_update)
        instance.is_published = validated_data.get(
            "is_published", instance.is_published
        )
        instance.cat_id = validated_data.get("cat_id", instance.cat_id)
        instance.save()
        # Здесь обязательно надо возвращать объект.
        return instance


# def decode():
#     # К нам поступает битовая строка, как JSON
#     stream = io.BytesIO(
#         b'{"title":"angelina jolie","content":"Content: Angelina jolie"}'
#     )
#     # мы ее парсим с помощью JSONParser
#     data = JSONParser().parse(stream)
#     print(data)  # это просто словарик, спарсированный
#     # потом отсылаем в сериализатор
#     serializer = WomenSerializer(data=data)
#     # там же и валидируем
#     serializer.is_valid()
#     # после отработки метода is_valid появляется validated_data, к которой
#     # можно обращаться
#     print(serializer.validated_data)  # а это уже OrderedDict
#
#
# def encode():
#     model = WomenModel("angelina jolie", "Content: Angelina jolie")
#     model_sr = WomenSerializer(model)
#     # model_sr.data здесь - это просто словарик
#     print(model_sr.data, type(model_sr.data), sep="\n")
#     # json - это байтовая строка
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#     # здесь мы просто преобразовали объект в словарь, а словарь - в строку.


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        # fields = "__all__" # Нельзя использовать __all__ вместе с exclude и подобным
        fields = ("title", "date", "get_absolute_url")
