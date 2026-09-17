from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase

from customers.models import Customer
from deliveries.models import Delivery
from subscriptions.models import PausePeriod, Subscription, SubscriptionCustomer


class SubscriptionBusinessFlowTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="customer1",
            email="customer1@example.com",
            password="StrongPass123!",
            role="CUSTOMER",
            phone="9876543210",
        )
        self.customer = Customer.objects.create(
            user=self.user,
            name="Rahul Sharma",
            phone="9876543210",
            email="rahul@example.com",
            address="A-101",
        )

    def test_pause_and_early_resume_shortens_pause_period(self):
        subscription = Subscription.objects.create(
            customer=self.customer,
            monthly_price=3000,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 30),
            status="ACTIVE",
        )
        subscription.generate_delivery_records()

        subscription.pause_subscription(date(2026, 9, 14), date(2026, 9, 18), "Travel")
        self.assertEqual(
            Delivery.objects.filter(subscription=subscription, delivery_date__range=[date(2026, 9, 14), date(2026, 9, 18)]).count(),
            5,
        )
        self.assertTrue(
            Delivery.objects.filter(
                subscription=subscription,
                delivery_date=date(2026, 9, 16),
                status="PAUSED",
            ).exists()
        )

        subscription.resume_subscription(date(2026, 9, 16))

        pause = PausePeriod.objects.get(subscription=subscription)
        self.assertEqual(pause.end_date, date(2026, 9, 15))
        self.assertEqual(Delivery.objects.get(subscription=subscription, delivery_date=date(2026, 9, 16)).status, "SCHEDULED")
        self.assertEqual(Delivery.objects.get(subscription=subscription, delivery_date=date(2026, 9, 17)).status, "SCHEDULED")

    def test_delivery_statuses_and_billing_proration(self):
        subscription = Subscription.objects.create(
            customer=self.customer,
            monthly_price=3000,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 30),
            status="ACTIVE",
        )
        subscription.generate_delivery_records()

        for delivery in Delivery.objects.filter(subscription=subscription, delivery_date__month=9):
            if delivery.delivery_date.day <= 20:
                delivery.status = "SERVED"
                delivery.save()

        bill = subscription.generate_monthly_bill(date(2026, 9, 1))
        self.assertEqual(bill.scheduled_days, 22)
        self.assertGreater(bill.served_days, 0)
        self.assertGreater(bill.total_amount, 0)

    def test_mid_cycle_transfer_preserves_history_and_splits_billing(self):
        User = get_user_model()
        second_user = User.objects.create_user(
            username="customer2",
            password="StrongPass123!",
            role="CUSTOMER",
            phone="9876543211",
        )
        second_customer = Customer.objects.create(
            user=second_user,
            name="Amit Verma",
            phone="9876543211",
        )
        subscription = Subscription.objects.create(
            customer=self.customer,
            monthly_price=3000,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 30),
        )
        subscription.generate_delivery_records()
        for delivery in subscription.deliveries.filter(delivery_date__lte=date(2026, 9, 15)):
            delivery.status = "SERVED"
            delivery.save(update_fields=["status"])

        subscription.transfer(second_customer, date(2026, 9, 16))

        first_period, second_period = SubscriptionCustomer.objects.filter(subscription=subscription)
        self.assertEqual(first_period.customer, self.customer)
        self.assertEqual(first_period.end_date, date(2026, 9, 15))
        self.assertEqual(second_period.customer, second_customer)
        self.assertEqual(second_period.start_date, date(2026, 9, 16))
        self.assertEqual(subscription.monthly_price, 3000)
        self.assertEqual(subscription.start_date, date(2026, 9, 1))
        self.assertEqual(subscription.end_date, date(2026, 9, 30))
        self.assertTrue(
            subscription.deliveries.filter(
                delivery_date=date(2026, 9, 15), customer=self.customer, status="SERVED"
            ).exists()
        )
        self.assertTrue(
            subscription.deliveries.filter(delivery_date=date(2026, 9, 16), customer=second_customer).exists()
        )

        for delivery in subscription.deliveries.filter(delivery_date__gte=date(2026, 9, 16)):
            delivery.status = "SERVED"
            delivery.save(update_fields=["status"])
        bills = subscription.generate_monthly_bills(date(2026, 9, 1))

        self.assertEqual(len(bills), 2)
        self.assertEqual({bill.customer_id for bill in bills}, {self.customer.id, second_customer.id})
        self.assertEqual(sum(bill.served_days for bill in bills), 22)


class SubscriptionTransferApiTests(APITestCase):
    def test_transfer_endpoint(self):
        User = get_user_model()
        owner = User.objects.create_user(username="owner", password="OwnerPass123!", role="OWNER", phone="9000000000")
        first_user = User.objects.create_user(username="first", password="FirstPass123!", role="CUSTOMER", phone="9000000001")
        second_user = User.objects.create_user(username="second", password="SecondPass123!", role="CUSTOMER", phone="9000000002")
        first_customer = Customer.objects.create(user=first_user, name="First Customer", phone="9000000001")
        second_customer = Customer.objects.create(user=second_user, name="Second Customer", phone="9000000002")
        subscription = Subscription.objects.create(
            customer=first_customer,
            monthly_price=3000,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 30),
        )
        subscription.generate_delivery_records()
        self.client.force_authenticate(owner)

        response = self.client.post(
            f"/api/subscriptions/{subscription.id}/transfer/",
            {"new_customer_id": second_customer.id, "transfer_date": "2026-09-16"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["to_customer"], second_customer.id)
