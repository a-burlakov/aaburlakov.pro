# для форм создают всегда вот такой как раз файл
from django import forms
from .models import *


class AddPostForm(forms.Form):
    # Атрибуты - это поля, которые будут отображаться на форме.
    # Они не должны копировать полностью то, что есть в модели.
    # Но желательно, конечно, чтобы названия совпадали.
    title = forms.CharField(
        max_length=255,
        label="Заголовок",
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )
    slug = forms.SlugField(max_length=255, label="URL")
    content = forms.CharField(
        widget=forms.Textarea(attrs={"cols": 60, "rows": 10}), label="Контент"
    )
    is_published = forms.BooleanField(label="Публикация", required=False, initial=True)
    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(), label="Категории", empty_label="не выбрано"
    )
