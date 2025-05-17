from rest_framework import serializers
from users.models import User, Payments


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ('course', 'lesson', 'amount', 'method', 'payment_session_id', 'payment_link')