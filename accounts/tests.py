from rest_framework.test import APITestCase

from accounts.models import User


class RegistrationApiTests(APITestCase):
    def test_customer_can_register(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "new-customer",
                "email": "new-customer@example.com",
                "phone": "9222222222",
                "password": "StrongPass123!",
                "role": "OWNER",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username="new-customer")
        self.assertEqual(user.role, "CUSTOMER")
        self.assertTrue(user.check_password("StrongPass123!"))
