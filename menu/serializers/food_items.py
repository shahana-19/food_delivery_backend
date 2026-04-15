from rest_framework import serializers
from ..models import FoodItems

class FoodItemsSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name")

    class Meta:
        model = FoodItems
        fields = [
            "id",
            "restaurant",
            "category",
            "category_name",
            "name",
            "description",
            "price",
            "image",
            "is_available",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]