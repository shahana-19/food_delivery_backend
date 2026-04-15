from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from menu.models import Category
from menu.serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_permissions(self):
        """
        - Anyone can view categories
        - Only restaurant owners can create/update/delete
        """
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """
        Public:
        - Categories of verified restaurants only

        Owner:
        - Categories of their own restaurants
        """
        user = self.request.user

        if user.is_authenticated and user.is_staff:
            return Category.objects.all()

        if user.is_authenticated and self.action not in ["list", "retrieve"]:
            return Category.objects.filter(
                restaurant__owner=user
            )

        return Category.objects.filter(
            restaurant__is_verified=True
        )

    def perform_create(self, serializer):
        restaurant = serializer.validated_data["restaurant"]

        if restaurant.owner != self.request.user:
            raise PermissionDenied(
                "You are not allowed to add categories to this restaurant."
            )

        serializer.save()
