from warnings import filters

from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend


from users.models import User, Payments
from users.serializers import UserSerializer, PaymentsSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class PaymentsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ('payment_date',)
    filterset_fields = ('course', 'lesson', 'method')
    permission_classes = [permissions.IsAuthenticated]


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [permissions.IsAuthenticated]


class TokenObtainView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]