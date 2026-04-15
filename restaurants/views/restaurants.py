from ..models import Restaurant
from rest_framework import viewsets, permissions, filters
from ..serializers import RestaurantSerializer

class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "city"]

    def get_queryset(self):
        user = self.request.user

        # Admin can see all
        if user.is_staff:
            return Restaurant.objects.all()

        # Public users see only verified restaurants
        if self.action in ["list", "retrieve"]:
            return Restaurant.objects.filter(is_verified=True)

        # Owners see their own restaurants
        return Restaurant.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

