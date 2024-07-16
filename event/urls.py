from django.urls import path
from event import views

urlpatterns = [
    path('', views.EventListCreateView.as_view(), name='event'),
    path('tickets/', views.TicketView.as_view(), name='ticket'),
    path('<int:event_id>/tickets/<int:ticket_id>/reserve/', views.TicketReserveView.as_view(), name='ticket-reserve'),
    path('<int:event_id>/tickets/<int:ticket_id>/purchase/', views.TicketPurchaseView.as_view(), name='ticket-purchase')
]