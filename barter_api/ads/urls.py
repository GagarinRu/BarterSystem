from django.urls import path

from .views import (
    AdListCreateView,
    AdRetrieveUpdateDestroyView,
    ExchangeProposalCreateView,
    ExchangeProposalUpdateView,
    UserProposalsListView
)


urlpatterns = [
    path(
        'ads/',
        AdListCreateView.as_view(),
        name='ad-list-create'
    ),
    path(
        'ads/<int:pk>/',
        AdRetrieveUpdateDestroyView.as_view(),
        name='ad-detail'
    ),
    path(
        'proposals/',
        ExchangeProposalCreateView.as_view(),
        name='proposal-create'
    ),
    path(
        'proposals/<int:pk>/',
        ExchangeProposalUpdateView.as_view(),
        name='proposal-update'
    ),
    path(
        'my-proposals/',
        UserProposalsListView.as_view(),
        name='user-proposals'
    ),
]
