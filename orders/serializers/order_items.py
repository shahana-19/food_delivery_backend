from rest_framework import serializers
from orders.models import OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    food_name = serializers.CharField(source="food_item.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",        
            "food_item",    
            "quantity",
            "price",
            "food_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
