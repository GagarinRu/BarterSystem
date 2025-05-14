from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
    CreateAPIView, ListAPIView, ListCreateAPIView,
    RetrieveUpdateDestroyAPIView, UpdateAPIView
)
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from .filters import AdFilter
from .models import Ad, ExchangeProposal
from .pagination import AdsPagination
from .serializers import (
    AdSerializer, ExchangeProposalSerializer,
    ExchangeProposaUpdatelSerializer
)


class AdListCreateView(ListCreateAPIView):
    """Endpoint для просмотра списка и создания объявлений."""

    queryset = Ad.objects.filter(is_active=True)
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AdFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    pagination_class = AdsPagination


class AdRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Endpoint для просмотра, обновления и удаления объявления."""

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        """Обновление объявления с проверкой прав доступа."""
        if serializer.instance.user != self.request.user:
            self.permission_denied(
                self.request,
                message="Вы не являетесь автором этого объявления"
            )
        serializer.save()

    def perform_destroy(self, instance):
        """Удаление объявление с выставлением неактивного статуса."""
        if instance.user != self.request.user:
            self.permission_denied(
                self.request,
                message="Вы не являетесь автором этого объявления"
            )
        instance.is_active = False
        instance.save()
        return Response(status=HTTP_204_NO_CONTENT)


class ExchangeProposalCreateView(CreateAPIView):
    """Endpoint для создания предложений обмена."""

    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Соаздние предложения обмена."""
        serializer.save(status='pending')


class ExchangeProposalUpdateView(UpdateAPIView):
    """Endpoint для обновления статуса предложения обмена."""

    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposaUpdatelSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """Обновление предложения обмена."""
        instance = self.get_object()
        if instance.ad_receiver.user != self.request.user:
            self.permission_denied(
                self.request,
                message="Только получатель может изменить статус предложения"
            )
        serializer.save()


class UserProposalsListView(ListAPIView):
    """Endpoint для просмотра предложений пользователя."""

    serializer_class = ExchangeProposalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        """Возвращает предложения, связанные с текущим пользователем."""
        user = self.request.user
        return ExchangeProposal.objects.filter(
            ad_receiver__user=user
        ) | ExchangeProposal.objects.filter(
            ad_sender__user=user
        ).select_related('ad_sender', 'ad_receiver')
