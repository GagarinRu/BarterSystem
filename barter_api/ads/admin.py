from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Ad, ExchangeProposal


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """Админ.панель объявлений."""

    empty_value_display = 'Нет Информации'


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    """Админ.панель предложений обмена."""

    empty_value_display = 'Нет Информации'


admin.site.unregister(Group)
admin.site.empty_value_display = 'Не задано'
