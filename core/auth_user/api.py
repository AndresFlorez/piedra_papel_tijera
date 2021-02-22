from django.contrib.auth import get_user_model
from rest_framework import static, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from .serializers import AuthUserSerializer

User = get_user_model()


class AuthUserAPI(viewsets.ModelViewSet):
    serializer_class = AuthUserSerializer
    queryset = User.objects.all().order_by('-last_login')
    pagination_class = PageNumberPagination
