import email
from rest_framework import viewsets, permissions, views, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Radiologist
from .serializers import RadiologistSerializer, LoginSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer

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
            return Response({"details", "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": f"Error invalidating token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
class PasswordResetRequestView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(request.data).data
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "OTP sent to your email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetConfirmView(views.APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)