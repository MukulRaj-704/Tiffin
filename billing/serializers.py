from rest_framework import serializers

from billing.models import Bill


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = [
            "id",
            "customer",
            "subscription",
            "billing_month",
            "monthly_price",
            "scheduled_days",
            "served_days",
            "paused_days",
            "skipped_days",
            "daily_rate",
            "total_amount",
            "status",
            "generated_at",
        ]
        read_only_fields = ["id", "generated_at"]
