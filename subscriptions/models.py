from datetime import date, timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models, transaction

from customers.models import Customer


class Subscription(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("PAUSED", "Paused"),
        ("CANCELLED", "Cancelled"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="subscriptions")
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.customer.name} - {self.start_date}"

    def get_delivery_dates(self):
        current = self.start_date
        dates = []
        while current <= self.end_date:
            if current.weekday() < 5:
                dates.append(current)
            current += timedelta(days=1)
        return dates

    def generate_delivery_records(self):
        from deliveries.models import Delivery

        for delivery_date in self.get_delivery_dates():
            Delivery.objects.get_or_create(
                subscription=self,
                delivery_date=delivery_date,
                defaults={"customer": self.customer, "status": "SCHEDULED"},
            )
        return self.deliveries.all()

    def ownership_for_date(self, ownership_date):
        ownership = self.customer_periods.filter(
            start_date__lte=ownership_date,
        ).filter(models.Q(end_date__isnull=True) | models.Q(end_date__gte=ownership_date)).first()
        return ownership.customer if ownership else self.customer

    @transaction.atomic
    def transfer(self, new_customer, transfer_date):
        from deliveries.models import Delivery

        if transfer_date < self.start_date or transfer_date > self.end_date:
            raise ValidationError("Transfer date must be inside the subscription cycle.")

        current = self.customer_periods.filter(
            start_date__lte=transfer_date,
        ).filter(models.Q(end_date__isnull=True) | models.Q(end_date__gte=transfer_date)).first()
        if not current:
            current = SubscriptionCustomer.objects.create(
                subscription=self,
                customer=self.customer,
                start_date=self.start_date,
                end_date=self.end_date,
            )
        if current.customer_id == new_customer.id:
            raise ValidationError("The subscription already belongs to this customer.")

        current.end_date = transfer_date - timedelta(days=1)
        current.save(update_fields=["end_date"])
        new_period = SubscriptionCustomer.objects.create(
            subscription=self,
            customer=new_customer,
            start_date=transfer_date,
            end_date=self.end_date,
        )
        SubscriptionTransfer.objects.create(
            subscription=self,
            from_customer=current.customer,
            to_customer=new_customer,
            transfer_date=transfer_date,
        )
        Delivery.objects.filter(
            subscription=self,
            delivery_date__gte=transfer_date,
            status__in=["SCHEDULED", "PAUSED"],
        ).update(customer=new_customer)
        return new_period

    def pause_subscription(self, start_date, end_date, reason=""):
        from deliveries.models import Delivery

        if self.status == "PAUSED":
            raise ValidationError("Subscription is already paused.")
        if start_date > end_date:
            raise ValidationError("Pause start date cannot be after end date.")
        if start_date < self.start_date or end_date > self.end_date:
            raise ValidationError("Pause period must be within subscription dates.")

        overlapping = PausePeriod.objects.filter(
            subscription=self,
            start_date__lte=end_date,
            end_date__gte=start_date,
        ).exists()
        if overlapping:
            raise ValidationError("Pause period overlaps with an existing pause.")

        pause_period = PausePeriod.objects.create(
            subscription=self,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
        )

        deliveries = Delivery.objects.filter(
            subscription=self,
            delivery_date__range=(start_date, end_date),
            delivery_date__week_day__in=[1, 2, 3, 4, 5],
        )
        for delivery in deliveries:
            if delivery.status != "SERVED":
                delivery.status = "PAUSED"
                delivery.save()

        self.status = "PAUSED"
        self.save()
        return pause_period

    def resume_subscription(self, resume_date):
        from deliveries.models import Delivery

        if not isinstance(resume_date, date):
            raise ValidationError("Resume date is invalid.")

        pause = PausePeriod.objects.filter(
            subscription=self,
            start_date__lte=resume_date,
            end_date__gte=resume_date,
        ).order_by("-start_date").first()

        if not pause:
            raise ValidationError("No active pause found for this subscription.")

        if resume_date < pause.start_date or resume_date > pause.end_date:
            raise ValidationError("Resume date must be inside the active pause period.")

        old_end = pause.end_date
        pause.end_date = resume_date - timedelta(days=1)
        pause.save()

        for delivery in Delivery.objects.filter(
            subscription=self,
            delivery_date__gte=resume_date,
            delivery_date__lte=old_end,
        ):
            if delivery.status == "PAUSED":
                delivery.status = "SCHEDULED"
                delivery.save()

        self.status = "ACTIVE"
        self.save()
        return pause

    def generate_monthly_bill(self, billing_month):
        bills = self.generate_monthly_bills(billing_month)
        return bills[0] if bills else None

    def generate_monthly_bills(self, billing_month):
        from billing.models import Bill
        from deliveries.models import Delivery

        month_start = billing_month.replace(day=1)
        next_month = (month_start.replace(day=28) + timedelta(days=4)).replace(day=1)
        scheduled = Delivery.objects.filter(
            subscription=self,
            delivery_date__gte=month_start,
            delivery_date__lt=next_month,
        )

        scheduled_days = scheduled.filter(status__in=["SCHEDULED", "SERVED", "PAUSED", "SKIPPED"]).count()
        daily_rate = Decimal("0")
        if scheduled_days:
            daily_rate = Decimal(str(self.monthly_price)) / Decimal(scheduled_days)

        bills = []
        customer_ids = set(scheduled.values_list("customer_id", flat=True))
        for customer_id in customer_ids:
            customer_deliveries = scheduled.filter(customer_id=customer_id)
            served_days = customer_deliveries.filter(status="SERVED").count()
            paused_days = customer_deliveries.filter(status="PAUSED").count()
            skipped_days = customer_deliveries.filter(status="SKIPPED").count()
            bill, _ = Bill.objects.update_or_create(
                customer_id=customer_id,
                subscription=self,
                billing_month=month_start,
                defaults={
                    "monthly_price": self.monthly_price,
                    "scheduled_days": customer_deliveries.filter(status__in=["SCHEDULED", "SERVED", "PAUSED", "SKIPPED"]).count(),
                    "served_days": served_days,
                    "paused_days": paused_days,
                    "skipped_days": skipped_days,
                    "daily_rate": daily_rate,
                    "total_amount": daily_rate * Decimal(served_days),
                    "status": "GENERATED",
                },
            )
            bills.append(bill)
        return bills


class PausePeriod(models.Model):
    subscription = models.ForeignKey("Subscription", on_delete=models.CASCADE, related_name="pause_periods")
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return f"{self.subscription.customer.name}: {self.start_date} to {self.end_date}"


class SubscriptionCustomer(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="customer_periods")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="subscription_periods")
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ["start_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["subscription", "customer", "start_date"],
                name="unique_subscription_customer_period_start",
            ),
        ]


class SubscriptionTransfer(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="transfers")
    from_customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="outgoing_subscription_transfers")
    to_customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="incoming_subscription_transfers")
    transfer_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["transfer_date", "created_at"]
