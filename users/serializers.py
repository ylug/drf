from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from users.models import Payment, User, Subscription


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    """Базовый ериализатор для модели подписки"""

    class Meta:
        model = Subscription
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    payment_list = PaymentSerializer(source='payment_set', many=True)

    class Meta:
        model = User
        fields = '__all__'
