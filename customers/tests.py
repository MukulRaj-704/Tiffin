from io import BytesIO

from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import User
from customers.models import Customer


class CustomerApiTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            password="owner-password",
            role="OWNER",
            phone="9000000000",
        )
        self.client.force_authenticate(self.owner)

    def test_owner_can_create_customer_profile_and_login_user(self):
        response = self.client.post(
            "/api/customers/",
            {
                "username": "customer-one",
                "password": "customer-password",
                "name": "Customer One",
                "phone": "9111111111",
                "email": "customer@example.com",
                "address": "10 Main Street",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "Customer One")
        self.assertTrue(Customer.objects.filter(phone="9111111111", user__username="customer-one").exists())


class CustomerImportTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="import-owner",
            password="OwnerPass123!",
            role="OWNER",
            phone="9000000010",
        )
        self.client.force_authenticate(self.owner)

    def test_import_normalizes_deduplicates_and_reports_rejections(self):
        csv_data = (
            "name,phone,start_date,monthly_price\n"
            "Rahul,9876543210,01/09/2026,3000\n"
            "Rahul Sharma,+91 98765 43210,2026-09-01,3000\n"
            "Amit,,15-09-2026,3000\n"
            "Priya,9876543212,invalid,3000\n"
            "Neha,9876543213,09.09.2026,2800\n"
        ).encode()
        upload = SimpleUploadedFile("customers.csv", BytesIO(csv_data).read(), content_type="text/csv")

        response = self.client.post("/api/import/customers/", {"file": upload}, format="multipart")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["imported"], 2)
        self.assertEqual(response.data["deduped"], 1)
        self.assertEqual(response.data["rejected"], 2)
        self.assertEqual(Customer.objects.filter(phone__in=["9876543210", "9876543213"]).count(), 2)
        self.assertEqual(len(response.data["errors"]), 2)