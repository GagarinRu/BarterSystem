from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ads'
    verbose_name = 'Объявление и предложение обмена'
    verbose_name_plural = 'Объявления и предложения обмена'
