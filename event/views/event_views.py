from django.db.models import Min
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from event.models import Event
from event.serializers import EventSerializer


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(operation_summary="이벤트 목록 조회"),
)
class EventListCreateView(ListCreateAPIView):
    queryset = Event.objects.all().annotate(min_price=Min('ticket__sale_price'))
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class EventDetailView(RetrieveAPIView):
    serializer_class = EventSerializer
    permission_classes = (AllowAny,)
    queryset = Event.objects.all().prefetch_related("ticket_set")
