from django.urls import path
from .views import (
    support_view, create_ticket_view, ticket_detail_view,
    faq_helpful_view, faq_view_count
)

urlpatterns = [
    path('', support_view, name='support'),
    path('ticket/create/', create_ticket_view, name='create_ticket'),
    path('ticket/<int:pk>/', ticket_detail_view, name='ticket_detail'),
    path('faq/<int:pk>/helpful/', faq_helpful_view, name='faq_helpful'),
    path('faq/<int:pk>/view/', faq_view_count, name='faq_view'),
]
