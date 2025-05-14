from django.contrib.auth import get_user_model
from rest_framework import serializers

from .constants import DESC_LENGHT_MIN, TITLE_LENGHT_MIN
from .models import Ad, ExchangeProposal
from .constants import STATUS_CHOICES

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = fields


class AdSerializer(serializers.ModelSerializer):
    """Сериализатор для модели объявлений."""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = [
            'id', 'user', 'title', 'description', 'image_url',
            'category', 'condition', 'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'user', 'created_at']

    def validate(self, data):
        """Валидация данных объявления."""
        if len(data.get('title', '')) < TITLE_LENGHT_MIN:
            raise serializers.ValidationError(
                f"Заголовок нужен минимум с {TITLE_LENGHT_MIN} символами"
            )
        if len(data.get('description', '')) < DESC_LENGHT_MIN:
            raise serializers.ValidationError(
                f"Описание  нужен минимум с {DESC_LENGHT_MIN} символами"
            )
        return data

    def create(self, validated_data):
        """Создание объявления с автоматическим назначением автора."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ExchangeProposalSerializer(serializers.ModelSerializer):
    """Сериализатор для модели предложений обмена."""

    ad_sender = AdSerializer(read_only=True)
    ad_receiver = AdSerializer(read_only=True)
    ad_sender_id = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.filter(is_active=True),
        write_only=True,
        source='ad_sender'
    )
    ad_receiver_id = serializers.PrimaryKeyRelatedField(
        queryset=Ad.objects.filter(is_active=True),
        write_only=True,
        source='ad_receiver'
    )
    status = serializers.ChoiceField(
        read_only=True,
        choices=STATUS_CHOICES
    )

    class Meta:
        model = ExchangeProposal
        fields = [
            'id', 'ad_sender', 'ad_receiver', 'ad_sender_id',
            'ad_receiver_id', 'comment', 'status', 'created_at'
        ]
        read_only_fields = [
            'id', 'ad_sender', 'status', 'ad_receiver', 'created_at'
        ]

    def validate(self, data):
        """Валидация данных предложения обмена."""
        ad_sender = data.get('ad_sender')
        ad_receiver = data.get('ad_receiver')
        request = self.context.get('request')
        if request.method == 'POST' and ExchangeProposal.objects.filter(
            ad_sender=ad_sender,
            ad_receiver=ad_receiver
        ).exists():
            raise serializers.ValidationError(
                "Вы уже отправляли предложение для этих объявлений"
            )
        if ad_sender.user != request.user:
            raise serializers.ValidationError(
                "Вы не являетесь владельцем объявления-отправителя"
            )
        return data


class ExchangeProposaUpdatelSerializer(serializers.ModelSerializer):
    """Сериализатор только для обновления статуса."""

    status = serializers.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = ExchangeProposal
        fields = ['status']
