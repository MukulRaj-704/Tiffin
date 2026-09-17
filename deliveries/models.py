from django.db import models

from customers.models import Customer
from subscriptions.models import Subscription


class Delivery(models.Model):
    STATUS_CHOICES = [
        ("SCHEDULED", "Scheduled"),
        ("SERVED", "Served"),
        ("PAUSED", "Paused"),
        ("SKIPPED", "Skipped"),
    ]

    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="deliveries")
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="deliveries", null=True)
    delivery_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="SCHEDULED")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("subscription", "delivery_date")
        ordering = ["delivery_date"]

    def __str__(self):
        customer_name = self.customer.name if self.customer_id else self.subscription.customer.name
        return f"{customer_name} - {self.delivery_date} - {self.status}"
