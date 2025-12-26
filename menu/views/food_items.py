from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import PermissionDenied
from ..models import Category, FoodItems
from ..serializers import FoodItemsSerializer
from restaurants.models import Restaurant

class FoodItemsViewSet(viewsets.ModelViewSet):
    serializer_class = FoodItemsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        # Admin can see all categories
        if user.is_staff:
            return FoodItems.objects.all()

        # Public users see only categories of verified restaurants
        if self.action in ["list", "retrieve"]:
            return FoodItems.objects.filter(restaurant__is_verified=True)
        # Owners see categories of their own restaurants
        return FoodItems.objects.filter(restaurant__owner=user)

    def perform_create(self, serializer):
        restaurant = serializer.validated_data['restaurant']

        if restaurant.owner != self.request.user:
            raise PermissionDenied("You do not have permission to add categories to this restaurant.")

        serializer.save()
