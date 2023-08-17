from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TagViewSet,
                    RecipyViewSet,
                    IngredientViewSet,
                    UserViewSet,
                    APIFollow,
                    APISet_Password,
                    )

app_name = "api"

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('recipes', RecipyViewSet, basename='recipes')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('users/subscriptions/', APIFollow.as_view()),
    path('users/set_password/', APISet_Password.as_view()),
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')), 

    path('auth/', include('djoser.urls.authtoken')),

]