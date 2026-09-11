import logging
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .schema import login_schema, profile_schema, register_schema, token_refresh_schema
from .serializers import RegisterSerializer, UserSerializer


logger = logging.getLogger(__name__)


@register_schema
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        
        logger.info("User created: id=%s", user.id)
    

@profile_schema
class CurrentUserAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@login_schema
class LoginAPIView(TokenObtainPairView):
    pass


@token_refresh_schema
class RefreshTokenAPIView(TokenRefreshView):
    pass


