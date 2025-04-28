from rest_framework.routers import DefaultRouter

from .views import AddressViewSet, DriverViewSet, ServiceViewSet

router = DefaultRouter()
router.register(r"addresses", AddressViewSet, basename="address")
router.register(r"drivers", DriverViewSet, basename="driver")
router.register(r"services", ServiceViewSet, basename="service")

urlpatterns = router.urls
