# Generated by Django 4.1.6 on 2023-02-04 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Название')),
                ('sub_title', models.CharField(blank=True, max_length=250, verbose_name='Подзаголовок')),
                ('image', models.ImageField(upload_to='article_images/', verbose_name='Главное изображение')),
                ('text', models.TextField(verbose_name='Текст')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('archived', models.BooleanField(verbose_name='Архив')),
                ('slug', models.SlugField(max_length=80, null=True, verbose_name='URL-путь')),
                ('article_type', models.CharField(choices=[('BL', 'Blog post'), ('PR', 'Project post')], default='BL', max_length=2, verbose_name='Тип')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Women',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('content', models.TextField(blank=True)),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=True)),
            ],
        ),
    ]
