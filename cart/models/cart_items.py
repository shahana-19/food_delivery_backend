# apps/cart/models/cart_item.py
from django.db import models
from .cart import Cart
from menu.models.food_items import FoodItems
from common.model.basemodel import BaseModel


class CartItem(BaseModel):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    food_item = models.ForeignKey(
        FoodItems,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "food_item")

    def __str__(self):
        return f"{self.food_item.name} x {self.quantity}"
