from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from ..models import User
from ..serializers import RegisterSerializer, UserSerializer

User = get_user_model()
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customize JWT token to include user details"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """JWT Login View"""
    serializer_class = CustomTokenObtainPairSerializer

class RegisterViewSet(viewsets.ModelViewSet):
    """
    Handles:
    - POST /users/ → Register new user
    - GET /users/profile/ → View current user profile
    - PUT /users/profile/ → Update profile
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ["create", "login"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    # 🧾 POST /users/ → Register
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens on registration
        refresh = RefreshToken.for_user(user)
        token_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response(
            {
                "message": "User registered successfully.",
                "user": UserSerializer(user).data,
                "tokens": token_data,
            },
            status=status.HTTP_201_CREATED,
        )

    # 👤 GET/PUT /users/profile/
    @action(detail=False, methods=["get", "put"], permission_classes=[IsAuthenticated])
    def profile(self, request):
        user = request.user

        if request.method == "GET":
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Profile updated successfully", "user": serializer.data},
            status=status.HTTP_200_OK,
        )
