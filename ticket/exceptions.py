from rest_framework.exceptions import APIException
from rest_framework import status


class NotEnoughTicketsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '남은 티켓이 없습니다.'

    def __init__(self, detail=None, code=None):
        self.detail = detail or self.default_detail