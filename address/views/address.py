from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from address.serializers.address import AddressSerializer
from ..models import Address



class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # If new address is default → unset others
        if serializer.validated_data.get("is_default"):
            Address.objects.filter(
                user=self.request.user,
                is_default=True
            ).update(is_default=False)

        serializer.save(user=self.request.user)
