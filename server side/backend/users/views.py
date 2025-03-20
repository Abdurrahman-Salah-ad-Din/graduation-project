from rest_framework import viewsets, permissions, views, status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Radiologist
from .serializers import RadiologistSerializer, LoginSerializer, PasswordResetRequestSerializer, OTPVerificationSerializer, PasswordUpdateSerializer 

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
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": f"Error invalidating token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
class BasePasswordResetView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = None
    success_message = "Success"

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"details": self.success_message}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(BasePasswordResetView):
    serializer_class = PasswordResetRequestSerializer
    success_message = "OTP sent to your email."

class OTPVerificationView(BasePasswordResetView):
    serializer_class = OTPVerificationSerializer
    success_message = "OTP verified. You can now reset your password."

class PasswordUpdateView(BasePasswordResetView):
    serializer_class= PasswordUpdateSerializer
    success_message = "Password has been reset."