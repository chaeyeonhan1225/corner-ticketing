from rest_framework.pagination import CursorPagination


class CommonCursorPagination(CursorPagination):
    page_size = 10
    page_size_query_param = 'size'
    ordering = '-created_at'