from django.apps import AppConfig


class PersonalSiteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.personal_site"
    verbose_name = "Мой личный сайт"
