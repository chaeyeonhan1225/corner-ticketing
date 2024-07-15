from django.urls import path
from ticket import views

urlpatterns = [
    path('', views.TicketView.as_view(), name='ticket'),
    path('<int:ticket_id>/reserve/', views.TicketReserveView.as_view(), name='ticket-reserve'),
    path('<int:ticket_id>/purchase/', views.TicketPurchaseView.as_view(), name='ticket-purchase')
]