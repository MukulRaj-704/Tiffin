from django.db import models

from customers.models import Customer
from deliveries.models import Delivery


class Notification(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="notifications")
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, related_name="notification")
    delivery_date = models.DateField()
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-delivery_date", "-created_at"]

    def __str__(self):
        return f"{self.customer.name} - {self.delivery_date}"