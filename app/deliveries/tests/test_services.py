from datetime import timedelta

from deliveries.models import Address, Driver, Service
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class ServiceTests(TestCase):

    def test_create_service(self):
        customer_address = Address.objects.create(
            street="789 Client Street", latitude=40.7128, longitude=-74.0060
        )
        driver_address = Address.objects.create(
            street="456 Driver Lane", latitude=40.7306, longitude=-73.9352
        )

        driver = Driver.objects.create(
            name="Driver One", current_address=driver_address
        )

        service = Service.objects.create(
            customer_address=customer_address,
            driver=driver,
            status="pending",
            estimated_arrival_time=timedelta(minutes=15),
        )

        self.assertEqual(Service.objects.count(), 1)
        self.assertEqual(service.customer_address.street, "789 Client Street")
        self.assertEqual(service.driver.name, "Driver One")
        self.assertEqual(service.status, "pending")
        self.assertEqual(service.estimated_arrival_time, timedelta(minutes=15))

    def test_str_method(self):
        customer_address = Address.objects.create(
            street="789 Client Street", latitude=40.7128, longitude=-74.0060
        )
        driver_address = Address.objects.create(
            street="456 Driver Lane", latitude=40.7306, longitude=-73.9352
        )

        driver = Driver.objects.create(
            name="Driver One", current_address=driver_address
        )

        service = Service.objects.create(
            customer_address=customer_address,
            driver=driver,
            status="pending",
            estimated_arrival_time=timedelta(minutes=15),
        )

        self.assertEqual(str(service), f"Service {service.id} - pending")


class ServiceAPITests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.customer_address = Address.objects.create(
            street="789 Client Street", latitude=40.7128, longitude=-74.0060
        )
        self.driver_address = Address.objects.create(
            street="456 Driver Lane", latitude=40.7306, longitude=-73.9352
        )

        self.driver = Driver.objects.create(
            name="Driver One", current_address=self.driver_address
        )

    def test_create_service(self):
        response = self.client.post(
            "/api/services/",
            {
                "customer_address": self.customer_address.id,
                "driver": self.driver.id,
                "status": "pending",
                "estimated_arrival_time": str(timedelta(minutes=15)),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Service.objects.count(), 1)

    def test_request_service(self):
        response = self.client.post(
            "/api/services/request_service/",
            {"address_id": self.customer_address.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Service.objects.count(), 1)
