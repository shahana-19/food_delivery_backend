from django.db import models
from common.model.basemodel import BaseModel
from restaurants.models.restaurants import Restaurant
from .category import Category

class FoodItems(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='food_items')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='food_items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='food_items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = 'food_items'
        ordering = ['-created_at']
        unique_together = ('restaurant', 'category', 'name')

    def __str__(self):
        return self.name

