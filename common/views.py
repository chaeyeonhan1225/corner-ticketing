import time

from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import threading


class ConcurrencyTestView(APIView):
    permission_classes = (AllowAny, )
    def do_long_task(self):
        sum = 0
        for i in range(0, 1_000_000):
            sum += (i%2)
        return sum

    def find_all_users(self):
        User = get_user_model()
        users = list(User.objects.all())
        time.sleep(1)
        return users

    def get(self, request):
        print(f'Request 1 {threading.currentThread().ident}')
        self.find_all_users()
        print(f'Request 2 {threading.currentThread().ident}')
        self.find_all_users()
        print(f'Request 3 {threading.currentThread().ident}')
        return Response({'message': 'Complete!'})