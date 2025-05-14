from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED,
    HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT
)
from rest_framework.test import APIClient

from .models import Ad, ExchangeProposal


class AdTestCase(TestCase):
    """Тестирование объявлений."""

    def setUp(self):
        """Получение данных для тестирования."""
        self.user1 = User.objects.create_user(
            username='user1', password='qwerty123'
        )
        self.user2 = User.objects.create_user(
            username='user2', password='qwerty123'
            )
        self.ad1 = Ad.objects.create(
            user=self.user1,
            title="Кофта из шерсти",
            description="Не ношеная кофта из шерсти",
            category="clothing",
            condition="new"
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title="Наушники",
            description="Беспроводные наушники",
            category="electronics",
            condition="used"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_create_ad(self):
        """Проверка создания объявления."""
        response = self.client.post('/api/ads/', {
            'title': 'Новое объявление',
            'description': 'Описание нового объявления',
            'category': 'other',
            'condition': 'new'
        }, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Ad.objects.count(), 3)
        self.assertEqual(Ad.objects.last().user, self.user1)

    def test_edit_ad_by_owner(self):
        """Проверка обновления владельцем объявления."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(f'/api/ads/{self.ad1.id}/', {
            'title': 'Обновленное название',
            'description': self.ad1.description,
            'category': self.ad1.category,
            'condition': self.ad1.condition
        }, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.ad1.refresh_from_db()
        self.assertEqual(self.ad1.title, 'Обновленное название')

    def test_edit_ad_by_non_owner(self):
        """Проверка обновления не владельцем объявления."""
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(f'/api/ads/{self.ad1.id}/', {
            'title': 'Попытка изменения',
            'description': self.ad1.description,
            'category': self.ad1.category,
            'condition': self.ad1.condition
        }, format='json')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_soft_delete_ad(self):
        """Проверка гкого удаления объявления с изменением 'is_active'."""
        initial_count = Ad.objects.filter(is_active=True).count()
        response = self.client.delete(f'/api/ads/{self.ad1.id}/')
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(
            Ad.objects.filter(is_active=True).count(),
            initial_count - 1
        )
        self.assertTrue(Ad.objects.get(id=self.ad1.id).is_active is False)


class ExchangeProposalTestCase(TestCase):
    """Тестирование предложений обмена."""

    def setUp(self):
        """Получение данных для тестирования."""
        self.user1 = User.objects.create_user(
            username='user1', password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2', password='password123'
        )
        self.ad1 = Ad.objects.create(
            user=self.user1,
            title="Книга по Python",
            description="Отличная книга для изучения Python",
            category="books",
            condition="new"
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title="Наушники",
            description="Беспроводные наушники",
            category="electronics",
            condition="used"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_create_proposal(self):
        """Проверка на статут 'pending'."""
        response = self.client.post('/api/proposals/', {
            'ad_sender_id': self.ad1.id,
            'ad_receiver_id': self.ad2.id,
            'comment': 'Предлагаю обмен'
        }, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(ExchangeProposal.objects.count(), 1)
        proposal = ExchangeProposal.objects.first()
        self.assertEqual(proposal.status, 'pending')
        self.assertEqual(proposal.ad_sender, self.ad1)
        self.assertEqual(proposal.ad_receiver, self.ad2)

    def test_update_proposal_status(self):
        """Проверка обновления статуса."""
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Тестовое предложение',
            status='pending'
        )
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(
            f'/api/proposals/{proposal.id}/',
            {'status': 'accepted'},
            format='json'
        )
        self.assertEqual(
            response.status_code,
            HTTP_200_OK,
            f"Ошибка: {response.data}"
        )
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, 'accepted')

    def test_update_proposal_status_by_non_receiver(self):
        """Попытка обновить статус предложения не получателем."""
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Тестовое предложение',
            status='pending'
        )
        response = self.client.patch(
            f'/api/proposals/{proposal.id}/',
            {'status': 'accepted'},
            format='json'
        )
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
