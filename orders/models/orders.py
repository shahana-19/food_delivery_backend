from django.db import models
from django.conf import settings
from restaurants.models.restaurants import Restaurant
from common.model.basemodel import BaseModel


class Order(BaseModel):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("placed", "Placed"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
        ("delivered", "Delivered"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    payment_status = models.BooleanField(default=False)

    class Meta:
        db_table = "orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} - {self.user}"
