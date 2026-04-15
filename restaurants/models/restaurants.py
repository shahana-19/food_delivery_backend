from django.db import models
from common.model.basemodel import BaseModel
from django.conf import settings

User = settings.AUTH_USER_MODEL
class Restaurant(BaseModel):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="restaurants"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_open = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "restaurants"
        ordering = ["-created_at"]