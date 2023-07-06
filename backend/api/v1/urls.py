from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, MyTokenObtainPairView, UpdatePassword

app_name = "api"

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('users/set_password/',
         UpdatePassword.as_view(),
         name='set password'),
    path('', include(router_v1.urls)),
    path('auth/token/',
         MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
]