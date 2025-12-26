from django.db import models
from common.model.basemodel import BaseModel
from restaurants.models.restaurants import Restaurant

class Category(BaseModel):
    restaurant=models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')
    name=models.CharField(max_length=255)


    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        unique_together = ('restaurant', 'name')

    def __str__(self):
        return self.name
