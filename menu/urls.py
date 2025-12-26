from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FoodItemsViewSet, CategoryViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="categories")
router.register("food-items", FoodItemsViewSet, basename="food-items")

urlpatterns = [
    path("", include(router.urls)),
]