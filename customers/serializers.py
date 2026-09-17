from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from customers.models import Customer

User = get_user_model()


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "user", "name", "phone", "email", "address", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class CustomerCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Customer
        fields = ["id", "username", "password", "name", "phone", "email", "address"]
        read_only_fields = ["id"]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        username = validated_data.pop("username")
        password = validated_data.pop("password")
        user = User.objects.create_user(
            username=username,
            password=password,
            email=validated_data.get("email", ""),
            phone=validated_data["phone"],
            role="CUSTOMER",
        )
        return Customer.objects.create(user=user, **validated_data)
