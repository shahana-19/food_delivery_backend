from rest_framework import serializers
from orders.models import Order
from .order_items import OrderItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "restaurant",
            "total_amount",
            "status",
            "payment_status",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
