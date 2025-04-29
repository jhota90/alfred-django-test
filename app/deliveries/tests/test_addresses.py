from deliveries.models import Address
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class AddressTests(TestCase):

    def test_create_address(self):
        address = Address.objects.create(
            street="123 Fake Street", latitude=40.7128, longitude=-74.0060
        )

        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(address.street, "123 Fake Street")
        self.assertEqual(address.latitude, 40.7128)
        self.assertEqual(address.longitude, -74.0060)

    def test_str_method(self):
        address = Address.objects.create(
            street="123 Fake Street", latitude=40.7128, longitude=-74.0060
        )

        self.assertEqual(str(address), "123 Fake Street")


class AddressViewSetTests(TestCase):
    def setUp(self):
        self.address_url = "/api/addresses/"
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.address = Address.objects.create(
            street="123 Test Street", latitude=40.7128, longitude=-74.0060
        )

    def test_list_addresses(self):
        response = self.client.get(self.address_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_address(self):
        url = f"{self.address_url}{self.address.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_address(self):
        payload = {
            "street": "456 New Street",
            "latitude": 41.1234,
            "longitude": -75.5678,
        }
        response = self.client.post(self.address_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_address(self):
        payload = {"street": "Updated Street"}
        url = f"{self.address_url}{self.address.id}/"
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_address(self):
        url = f"{self.address_url}{self.address.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
