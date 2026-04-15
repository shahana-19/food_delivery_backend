from rest_framework import serializers
from ..models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "owner",
            "owner_email",
            "name",
            "description",
            "address",
            "city",
            "latitude",
            "longitude",
            "is_open",
            "is_verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["owner", "is_verified", "created_at", "updated_at"]
