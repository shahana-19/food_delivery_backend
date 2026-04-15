from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer



class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    # -----------------------------------
    # POST /v1/orders/checkout/
    # -----------------------------------
    @action(detail=False, methods=["post"])
    def checkout(self, request):
        cart = Cart.objects.filter(
            user=request.user, is_active=True
        ).first()

        if not cart:
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_items = CartItem.objects.filter(cart=cart)

        total = sum(
            item.food_item.price * item.quantity
            for item in cart_items
        )

        order = Order.objects.create(
            user=request.user,
            restaurant=cart.restaurant,
            total_amount=total,
            status="placed",
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                food_item=item.food_item,
                quantity=item.quantity,
                price=item.food_item.price,
            )

        # deactivate cart
        cart.is_active = False
        cart.save()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )
