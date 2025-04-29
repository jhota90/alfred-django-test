from datetime import datetime

from deliveries.helpers import calculate_distance, calculate_estimated_arrival_time
from deliveries.models import Address, Driver, Service
from deliveries.serializers import (
    AddressSerializer,
    DriverSerializer,
    ServiceSerializer,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    @action(detail=True, methods=["post"])
    def complete_service(self, request, pk=None):
        """Permitir que un conductor marque un servicio como completado."""
        driver = self.get_object()
        service_id = request.data.get("service_id")

        try:
            service = Service.objects.get(id=service_id, driver=driver)
            service.status = "completed"
            service.finished_at = datetime.now()
            service.save()
            return Response({"status": "service completed"})
        except Service.DoesNotExist:
            return Response(
                {"error": "Service not found or unauthorized"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    @action(detail=False, methods=["post"])
    def request_service(self, request):
        """API para solicitar un servicio."""
        customer_address_id = request.data.get("address_id")

        try:
            customer_address = Address.objects.get(id=customer_address_id)
        except Address.DoesNotExist:
            return Response(
                {"error": "Address not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        disable_driver_ids = Service.objects.filter(status="pending").values_list(
            "driver_id", flat=True
        )

        drivers = Driver.objects.exclude(id__in=disable_driver_ids).select_related(
            "current_address"
        )
        if not drivers:
            return Response(
                {"error": "No drivers available"}, status=status.HTTP_400_BAD_REQUEST
            )

        nearest_driver = min(
            drivers,
            key=lambda driver: calculate_distance(
                customer_address.latitude,
                customer_address.longitude,
                driver.current_address.latitude,
                driver.current_address.longitude,
            ),
        )

        distance = calculate_distance(
            customer_address.latitude,
            customer_address.longitude,
            nearest_driver.current_address.latitude,
            nearest_driver.current_address.longitude,
        )

        estimated_arrival_time = calculate_estimated_arrival_time(distance)

        service = Service.objects.create(
            customer_address=customer_address,
            driver=nearest_driver,
            estimated_arrival_time=estimated_arrival_time,
        )

        serializer = self.get_serializer(service)
        return Response(
            {
                "driver": nearest_driver.name,
                "distance_km": round(distance, 2),
                "estimated_arrival_time_minutes": (
                    estimated_arrival_time.total_seconds() / 60
                ),
                "service_details": serializer.data,
            }
        )
