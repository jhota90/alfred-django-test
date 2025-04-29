from deliveries.models import Address, Driver
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class DriverTests(TestCase):

    def test_create_driver(self):
        address = Address.objects.create(
            street="123 Main Avenue", latitude=40.7128, longitude=-74.0060
        )

        driver = Driver.objects.create(name="John Doe", current_address=address)

        self.assertEqual(Driver.objects.count(), 1)
        self.assertEqual(driver.name, "John Doe")
        self.assertEqual(driver.current_address.street, "123 Main Avenue")

    def test_str_method(self):
        address = Address.objects.create(
            street="123 Main Avenue", latitude=40.7128, longitude=-74.0060
        )
        driver = Driver.objects.create(name="John Doe", current_address=address)

        self.assertEqual(str(driver), "John Doe")


class DriverViewSetTests(TestCase):
    def setUp(self):
        self.driver_url = "/api/drivers/"
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.address = Address.objects.create(
            street="789 Driver Street", latitude=40.7128, longitude=-74.0060
        )

        self.driver = Driver.objects.create(
            name="Test Driver", current_address=self.address
        )

    def test_list_drivers(self):
        response = self.client.get(self.driver_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_driver(self):
        url = f"{self.driver_url}{self.driver.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_driver(self):
        payload = {"name": "New Driver", "current_address": self.address.id}
        response = self.client.post(self.driver_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_driver(self):
        payload = {"name": "Updated Driver Name"}
        url = f"{self.driver_url}{self.driver.id}/"
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_driver(self):
        url = f"{self.driver_url}{self.driver.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
