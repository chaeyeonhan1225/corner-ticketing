from django.urls import path
from event.views import event_views, ticket_views, ticket_purchase_views

urlpatterns = [
    path('', event_views.EventListCreateView.as_view(), name='event-list'),
    path('<int:event_id>/tickets/', ticket_views.TicketListCreateView.as_view(), name='event-list'),
    path('<int:pk>/', event_views.EventDetailView.as_view(), name='event-detail'),
    # path('tickets/', ticket_views.TicketView.as_view(), name='ticket'),
    # path('<int:event_id>/tickets/<int:ticket_id>/reserve/', views.TicketReserveView.as_view(), name='ticket-reserve'),
    path('<int:event_id>/tickets/<int:ticket_id>/purchase/',
         ticket_purchase_views.TicketPurchaseView.as_view(), name='ticket-purchase')
]