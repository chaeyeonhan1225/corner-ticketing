from django.urls import path, include
from user import views


urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user-registration'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('tickets/', views.UserTicketView.as_view(), name='user-ticket'),
    path('tickets/<uuid:user_ticket_id>', views.UserTicketDetailView.as_view(), name='user-ticket')
]