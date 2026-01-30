from rest_framework import serializers
from ..models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id', 'user', 'full_name', 'phone', 'address_line',
            'city', 'state', 'pincode', 'is_default'
        ]
        read_only_fields = ['id', 'user']