from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterViewSet, CustomTokenObtainPairView, UserViewSet


router = DefaultRouter()
router.register("users", RegisterViewSet, basename="users")
router.register("manage-users", UserViewSet, basename=" manage-users")


urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
    
    
]
