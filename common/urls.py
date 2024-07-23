from django.urls import path

from common import views

urlpatterns = [path("", views.ConcurrencyTestView.as_view(), name="index")]
