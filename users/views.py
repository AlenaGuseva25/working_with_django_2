from itertools import product
from lib2to3.fixes.fix_input import context
from warnings import filters

import stripe
from requests import session
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend

from users import serializers
from users.models import User, Payments
from users.serializers import UserSerializer, PaymentsSerializer
from users.services import create_stripe_price, create_stripe_product, \
    create_stripe_session


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


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        payment = serializer.save(user=self.request.user)

        product_name = payment.course.name if payment.course else payment.lesson.name

        product = create_stripe_product(product_name)
        price = create_stripe_price(payment.amount, product.id)
        session = create_stripe_session(price.id)

        payment.payment_session_id = session.id
        payment.payment_link = session.url
        payment.save()


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