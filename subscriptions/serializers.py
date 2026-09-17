from rest_framework import serializers

from subscriptions.models import PausePeriod, Subscription, SubscriptionCustomer, SubscriptionTransfer


class SubscriptionSerializer(serializers.ModelSerializer):
    customer_periods = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    transfers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Subscription
        fields = [
            "id",
            "customer",
            "monthly_price",
            "start_date",
            "end_date",
            "status",
            "created_at",
            "updated_at",
            "customer_periods",
            "transfers",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class PausePeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PausePeriod
        fields = ["id", "subscription", "start_date", "end_date", "reason", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class SubscriptionCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionCustomer
        fields = ["id", "subscription", "customer", "start_date", "end_date"]


class SubscriptionTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionTransfer
        fields = ["id", "subscription", "from_customer", "to_customer", "transfer_date", "created_at"]
        read_only_fields = ["id", "created_at"]
