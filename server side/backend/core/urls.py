from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import PasswordUpdateView, RadiologistViewSet, LoginView, LogoutView, PasswordResetRequestView, OTPVerificationView
from rest_framework_simplejwt.views import TokenRefreshView
from patients.views import PatientViewSet
from scans.views import PatientScanView
from drf_spectacular.views import SpectacularRedocView
from django.http import FileResponse
import os

def openapi_yaml_view(request):
    """
    Serve the OpenAPI YAML file.
    """
    file_path = os.path.join(os.path.dirname(__file__), 'file.yaml')
    with open(file_path, 'rb') as f:
        return FileResponse(f, content_type='text/yaml')

router = DefaultRouter()
router.register(r'users', RadiologistViewSet)
router.register(r'scans', PatientScanView)
router.register(r'patients', PatientViewSet)

user_patterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/', OTPVerificationView.as_view(), name='otp_verification'),
    path('password-update/', PasswordUpdateView.as_view(), name='password_update'),
]

urlpatterns = [
    # Admin endpoint
    path('admin/', admin.site.urls),
    
    # User endpoints (grouped)
    path('users/', include((user_patterns, 'users'))),
    
    # Documentation endpoints
    path('doc.yaml', openapi_yaml_view, name='openapi-file'),
    path('documentation/', SpectacularRedocView.as_view(url_name='openapi-file'), name='redoc'),
    
    # Silk profiling
    path('silk/', include('silk.urls', namespace='silk')),
]

urlpatterns += router.urls