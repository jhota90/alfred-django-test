from django.db import models


class Address(models.Model):
    street = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.street


class Driver(models.Model):
    name = models.CharField(max_length=255)
    current_address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
    )

    customer_address = models.ForeignKey(
        Address, related_name="customer_services", on_delete=models.DO_NOTHING
    )
    driver = models.ForeignKey(Driver, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    estimated_arrival_time = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        return f"Service {self.id} - {self.status}"
