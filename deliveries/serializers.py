from rest_framework import serializers

from deliveries.models import Delivery


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ["id", "subscription", "customer", "delivery_date", "status", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
