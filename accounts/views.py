from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from .serializers import RegistrationSerializer
from rest_framework import generics

from accounts.models import Account


class MyCustomPagination(PageNumberPagination):
    page_size = 5


class RegistrationView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Account.objects.all()
    serializer_class = RegistrationSerializer