# для форм создают всегда вот такой как раз файл
from django import forms
from django.core.exceptions import ValidationError

from .models import *


class AddPostForm(forms.ModelForm):
    # Атрибуты - это поля, которые будут отображаться на форме.
    # Они не должны копировать полностью то, что есть в модели.
    # Но желательно, конечно, чтобы названия совпадали.
    # title = forms.CharField(
    #     max_length=255,
    #     label="Заголовок",
    #     widget=forms.TextInput(attrs={"class": "form-input"}),
    # )
    # slug = forms.SlugField(max_length=255, label="URL")
    # content = forms.CharField(
    #     widget=forms.Textarea(attrs={"cols": 60, "rows": 10}), label="Контент"
    # )
    # is_published = forms.BooleanField(label="Публикация", required=False, initial=True)
    # cat = forms.ModelChoiceField(
    #     queryset=Category.objects.all(), label="Категории", empty_label="не выбрано"
    # )

    #  Но можно просто связать с моделью
    class Meta:
        model = Women
        fields = ["title", "slug", "content", "photo", "is_published", "cat"]
        # widgets используется для того, чтобы указать стиль оформления для каждого поля
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "content": forms.Textarea(attrs={"cols": 60, "rows": 10}),
        }

    # Мы тут вызываем конструктор. И при этом после этого можем немного
    # отредактировать элементы формы.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cat"].empty_label = "Категория не выбрана"

    # валидация полей формы выполняется в отдельных методах вида clead_название
    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) > 100:
            raise ValidationError("Длина превышает 100 символов")

        return title
