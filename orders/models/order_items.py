
from django.db import models
from common.model.basemodel import BaseModel
from menu.models import FoodItems
from .orders import Order


class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    food_item = models.ForeignKey(
        FoodItems,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "order_items"

    def __str__(self):
        return f"{self.food_item} x {self.quantity}"

