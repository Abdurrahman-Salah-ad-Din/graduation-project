from django.urls import path, include
from rest_framework import routers
from .views import PatientViewSet

router = routers.DefaultRouter()
router.register(r'', PatientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]