from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Cart, CartItem
from ..serializers import CartSerializer, CartItemSerializer
from menu.models import FoodItems


class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # 🔹 Get or create active cart
    def get_cart(self, user, restaurant):
        cart, _ = Cart.objects.get_or_create(
            user=user,
            restaurant=restaurant,
            is_active=True,
        )
        return cart

    # -------------------------------------------------
    # GET /api/cart/
    # -------------------------------------------------
    def list(self, request):
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        if not cart:
            return Response({"detail": "Cart is empty"})
        return Response(CartSerializer(cart).data)

    # -------------------------------------------------
    # POST /api/cart/add/
    # -------------------------------------------------
    @action(detail=False, methods=["post"])
    def add(self, request):
        food_id = request.data.get("food_item")
        quantity = int(request.data.get("quantity", 1))

        food = FoodItems.objects.get(id=food_id)

        # Ensure one restaurant rule
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        if cart and cart.restaurant != food.restaurant:
            return Response(
                {"error": "Cart contains items from another restaurant"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = self.get_cart(request.user, food.restaurant)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            food_item=food,
        )
        if not created:
            cart_item.quantity += quantity
        cart_item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

    # -------------------------------------------------
    # PATCH /api/cart/item/{id}/
    # -------------------------------------------------
    @action(detail=True, methods=["patch"])
    def update_item(self, request, pk=None):
        item = CartItem.objects.get(id=pk, cart__user=request.user)
        item.quantity = request.data.get("quantity", item.quantity)
        item.save()
        return Response(CartItemSerializer(item).data)

    # -------------------------------------------------
    # DELETE /api/cart/item/{id}/
    # -------------------------------------------------
    @action(detail=True, methods=["delete"])
    def remove_item(self, request, pk=None):
        item = CartItem.objects.get(id=pk, cart__user=request.user)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # -------------------------------------------------
    # DELETE /api/cart/clear/
    # -------------------------------------------------
    @action(detail=False, methods=["delete"])
    def clear(self, request):
        Cart.objects.filter(user=request.user, is_active=True).delete()
        return Response({"message": "Cart cleared"})
