from django.db import models
from django.contrib.auth import get_user_model

from .constants import (
    CATEGORY_CHOICES, CONDITION_CHOICES, STATUS_CHOICES,
    TITLE_LENGHT_MAX, LENGHT_MAX, STATUS_LENGHT_MAX
)


User = get_user_model()


class Ad(models.Model):
    """Модель объявлений."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ads',
        verbose_name='Автор объявления'
    )
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=TITLE_LENGHT_MAX
    )
    description = models.TextField(
        verbose_name='Описание товара',
    )
    image_url = models.URLField(
        verbose_name='URL изображения',
        blank=True,
        null=True
    )
    category = models.CharField(
        verbose_name='Категория',
        max_length=LENGHT_MAX,
        choices=CATEGORY_CHOICES
    )
    condition = models.CharField(
        verbose_name='Состояние',
        max_length=LENGHT_MAX,
        choices=CONDITION_CHOICES
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активно'
    )

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f'{self.title}'

    def delete(self, *args, **kwargs):
        """Удаление путем изменение статуса на неактивный."""
        self.is_active = False
        self.save()


class ExchangeProposal(models.Model):
    """Модель предложений обмена."""

    ad_sender = models.ForeignKey(
        Ad,
        verbose_name='Объявление отправителя',
        on_delete=models.CASCADE,
        related_name='sent_proposals'
    )
    ad_receiver = models.ForeignKey(
        Ad,
        verbose_name='Объявление получателя',
        on_delete=models.CASCADE,
        related_name='received_proposals'
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True
    )
    status = models.CharField(
        max_length=STATUS_LENGHT_MAX,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Обмен предложением'
        verbose_name_plural = 'Обмен предложениями'
        ordering = ('-created_at',)
        constraints = [
            models.UniqueConstraint(
                fields=['ad_sender', 'ad_receiver'],
                name='unique_proposal'
            )
        ]

    def __str__(self):
        return f"Предложение #{self.id}: {self.ad_sender}->{self.ad_receiver}"
