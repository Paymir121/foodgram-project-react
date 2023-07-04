from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (RegistrationAPIView,
                    UserViewSet,
                    get_jwt_token,
                    )

app_name = "api"

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

auth_urlpatterns = [
    path('signup/', RegistrationAPIView.as_view()),
    path('token/',
         get_jwt_token,
         name='token_obtain_pair'),
]

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_urlpatterns))
]
