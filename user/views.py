from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from enumfields.drf.serializers import EnumSupportSerializerMixin

from ticket.models import Ticket, UserTicket
from user.tasks import send_joined_email

User = get_user_model()

class UserRegisterSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(
            **validated_data
        )

class UserLoginSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class UserProfileSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'nickname', 'created_at', 'updated_at', 'status']

class UserRegisterView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token: Token = TokenObtainPairSerializer.get_token(user)
            send_joined_email.delay(user.id)
            return Response(
                {
                    'user': serializer.data,
                    'token': {
                        'access': str(token.access_token),
                        'refrest': str(token)
                    }
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        token_serializer = TokenObtainPairSerializer(data=request.data)
        if token_serializer.is_valid():
            user = token_serializer.user
            serializer = UserLoginSerializer(user)
            return Response(
                {
                    'user': serializer.data,
                    'token': token_serializer.validated_data
                },
                status=status.HTTP_200_OK
            )

        return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(UserProfileSerializer(request.user).data)


# TODO: UserTicketSerializer 고도화 추가
class UserTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTicket
        fields = '__all__'


class UserTicketView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserTicketSerializer

    # TODO: 날짜 기준 필터링 추가
    def get_queryset(self):
        return UserTicket.objects.filter(owner=self.request.user)
