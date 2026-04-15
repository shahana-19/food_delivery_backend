from ..models import Category
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'restaurant', 'name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        