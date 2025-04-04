from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import PasswordUpdateView, RadiologistViewSet, LoginView, LogoutView, PasswordResetRequestView, OTPVerificationView
from rest_framework_simplejwt.views import TokenRefreshView
from patients.views import PatientViewSet
from scans.views import PatientScanView
from drf_spectacular.views import SpectacularRedocView
from django.http import FileResponse, Http404
from django.conf.urls.static import static
from django.conf import settings
import os

def openapi_yaml_view(request):
    """
    Returns the OpenAPI YAML documentation as a file response.

    The YAML file is expected to be in the same directory as this module.
    Note: We intentionally open the file without a context manager since
    FileResponse manages the file closing.
    """
    # Build the absolute path to the YAML documentation.
    file_path = os.path.join(os.path.dirname(__file__), 'doc.yaml')
    
    # Check if the file exists; if not, raise a 404 error.
    if not os.path.exists(file_path):
        raise Http404("YAML documentation not found.")

    # Open the file in binary mode.
    file_handle = open(file_path, 'rb')
    
    # Return a FileResponse with the appropriate content type.
    return FileResponse(file_handle, content_type='text/yaml')

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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)