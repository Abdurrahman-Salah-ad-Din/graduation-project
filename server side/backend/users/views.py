from rest_framework import viewsets, permissions, views, status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Radiologist
from .serializers import RadiologistSerializer, LoginSerializer, PasswordResetRequestSerializer, OTPVerificationSerializer, PasswordUpdateSerializer 
from core.exceptions import AppException
from core.errors import ErrorCodes
from core.error_messages import ERROR_MESSAGES

class RadiologistViewSet(viewsets.ModelViewSet):
    queryset = Radiologist.objects.all()
    serializer_class = RadiologistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        radiologists = super().get_queryset()
        if not self.request.user.is_staff:
            radiologists = radiologists.filter(id=self.request.user.id)
        return radiologists
    
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Get the refresh token from the request data
            refresh_token = request.data.get('refresh_token')

            if not refresh_token:
                # If refresh token is not provided, return an error
                return Response(
                {
                    "is_success": False,
                    "data": None,
                    "errors": [{
                        "code": ErrorCodes.AUTH_008,
                        "message": ERROR_MESSAGES[ErrorCodes.AUTH_008],
                        "field": "refresh_token",
                    }]
                },
                status=status.HTTP_400_BAD_REQUEST
            )

            # Process the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            # If the token is successfully blacklisted, return a success message
            return Response({
                "is_success": True,
                "data": {"details": "Logout successful."},
                "errors": None
            }, status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            # Catch any exception that occurs and format it as a custom error
            return Response({
                "is_success": False,
                "data": None,
                "errors": [{
                    "code": "USER_002",
                    "message": str(e),
                    "field": "refresh_token"
                }]
            }, status=status.HTTP_400_BAD_REQUEST)
        
class BasePasswordResetView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = None
    success_message = "Success"
    error_code = None

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"is_success": True, "errors": None, "data": self.success_message}, status=status.HTTP_200_OK)

class PasswordResetRequestView(BasePasswordResetView):
    serializer_class = PasswordResetRequestSerializer
    success_message = "OTP sent to your email."
    
class OTPVerificationView(BasePasswordResetView):
    serializer_class = OTPVerificationSerializer
    success_message = "OTP verified. You can now reset your password."

class PasswordUpdateView(BasePasswordResetView):
    serializer_class= PasswordUpdateSerializer
    success_message = "Password has been reset."