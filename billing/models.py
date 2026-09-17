from datetime import date
from decimal import Decimal

from django.db import models

from customers.models import Customer
from subscriptions.models import Subscription


class Bill(models.Model):
    STATUS_CHOICES = [
        ("GENERATED", "Generated"),
        ("UNPAID", "Unpaid"),
        ("PARTIALLY_PAID", "Partially Paid"),
        ("PAID", "Paid"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="bills")
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="bills")
    billing_month = models.DateField()
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)
    scheduled_days = models.IntegerField(default=0)
    served_days = models.IntegerField(default=0)
    paused_days = models.IntegerField(default=0)
    skipped_days = models.IntegerField(default=0)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="GENERATED")
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("customer", "subscription", "billing_month")
        ordering = ["-billing_month"]

    def __str__(self):
        return f"{self.customer.name} - {self.billing_month} - {self.total_amount}"
