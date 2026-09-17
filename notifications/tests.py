from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from customers.models import Customer
from deliveries.models import Delivery
from notifications.models import Notification
from subscriptions.models import Subscription


class NotificationOutboxTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="notification-customer",
            password="StrongPass123!",
            role="CUSTOMER",
            phone="9888888888",
        )
        self.customer = Customer.objects.create(user=user, name="Notification Customer", phone="9888888888")
        self.subscription = Subscription.objects.create(
            customer=self.customer,
            monthly_price=3000,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 30),
        )
        self.subscription.generate_delivery_records()

    def test_active_weekday_creates_one_idempotent_notification(self):
        first = self.client.post("/clock", {"date": "2026-09-17"}, content_type="application/json")
        second = self.client.post("/clock", {"date": "2026-09-17"}, content_type="application/json")

        self.assertEqual(first.status_code, 200)
        self.assertEqual(len(first.json()), 1)
        self.assertEqual(second.json(), [])
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(self.client.get("/outbox").json()[0]["customer_id"], self.customer.id)

    def test_paused_cancelled_and_weekend_deliveries_are_excluded(self):
        self.subscription.pause_subscription(date(2026, 9, 17), date(2026, 9, 17))
        paused = self.client.post("/clock", {"date": "2026-09-17"}, content_type="application/json")
        self.assertEqual(paused.json(), [])

        self.subscription.status = "CANCELLED"
        self.subscription.save(update_fields=["status"])
        cancelled = self.client.post("/clock", {"date": "2026-09-18"}, content_type="application/json")
        self.assertEqual(cancelled.json(), [])

        weekend = self.client.post("/clock", {"date": "2026-09-19"}, content_type="application/json")
        self.assertEqual(weekend.json(), [])