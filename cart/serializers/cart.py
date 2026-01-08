from rest_framework import serializers
from ..models import Cart
from .cart_items import CartItemSerializer


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "restaurant",
            "items",
            "total_price",
        ]

    def get_total_price(self, obj):
        return sum(
            item.food_item.price * item.quantity
            for item in obj.items.all()
        )
