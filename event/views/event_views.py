from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from event.models import Event
from event.serializers import EventSerializer


class EventListCreateView(ListCreateAPIView):
    queryset = Event.objects.all().prefetch_related("ticket_set")
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class EventDetailView(RetrieveAPIView):
    serializer_class = EventSerializer
    permission_classes = (AllowAny,)
    queryset = Event.objects.all().prefetch_related("ticket_set")
