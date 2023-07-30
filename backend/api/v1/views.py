from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import filters, mixins, status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.viewsets import GenericViewSet, ModelViewSet
import csv
from django.http import HttpResponse
from users.models import User, Follow
from recipy.models import Tag, Ingredient, Recipy, Favorite, ShoppingCart
from .permissions import (IsAdmin,
                          IsAdminOrReadOnly,
                          IsAuthorAdminModerOrReadOnly)
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import ConfirmationUserTokenSerializer, RecipyIngredient, RecipyFavoriteReadSerializer, UserSerializer, ChangePasswordSerializer, TagSerializer, RecipyReadSerializer, IngredientSerializer, RecipyWriteSerializer


class TagViewSet(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
    lookup_field = 'id'
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipyViewSet(ModelViewSet):
    serializer_class = RecipyReadSerializer
    permission_classes = (AllowAny,)
    queryset = Recipy.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipyReadSerializer
        return RecipyWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated, ],
        url_path=r'favorite'
    )
    def favorite(self, request, pk=None):
        user = get_object_or_404(User, username=self.request.user)
        recipy = get_object_or_404(Recipy, id=pk)
        if request.method == 'DELETE':
            Favorite.objects.filter(recipy=recipy, user=user).delete()
        if request.method == 'POST':
            Favorite.objects.create(recipy=recipy, user=user)
        serializer = RecipyFavoriteReadSerializer(recipy)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated, ],
        url_path=r'shopping_cart'
    )
    def shopping_cart(self, request, pk=None):
        user = get_object_or_404(User, username=self.request.user)
        recipy = get_object_or_404(Recipy, id=pk)
        if request.method == 'DELETE':
            ShoppingCart.objects.filter(recipy=recipy, user=user).delete()
        if request.method == 'POST':
            ShoppingCart.objects.create(recipy=recipy, user=user)
        serializer = RecipyFavoriteReadSerializer(recipy)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(
        detail=False,
        methods=['get',],
        permission_classes=[IsAuthenticated, ],
        url_path=r'download_shopping_cart'
    )
    def download_shopping_cart(self, request):
        user = get_object_or_404(User, username=self.request.user)
        shoping_carts = ShoppingCart.objects.filter(user=user)
        ingredients_in_shopping_cart = (dict())
        response = HttpResponse(content_type="text/csv",
                        headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},)
        writer = csv.writer(response)
        for shoping_cart in shoping_carts:
            ingredients_in_recipy = RecipyIngredient.objects.filter(recipy=shoping_cart.recipy)
            for ingredient_in_recipy in ingredients_in_recipy:
                name = ingredient_in_recipy.ingredients.name
                amount = ingredient_in_recipy.amount
                measurement_unit = ingredient_in_recipy.ingredients.measurement_unit

                if name not in ingredients_in_shopping_cart:
                    ingredients_in_shopping_cart[name] = {'amount': amount,
                                                        'measurement_unit': measurement_unit}
                else:
                    ingredients_in_shopping_cart[name]['amount']  += amount
        for name in ingredients_in_shopping_cart:
            amount = ingredients_in_shopping_cart[name]['amount']
            measurement_unit = ingredients_in_shopping_cart[name]['measurement_unit']
            writer.writerow([name, amount, measurement_unit])
        ShoppingCart.objects.filter(user=user).delete()
        return response


class IngredientViewSet(ModelViewSet):
    lookup_field = 'id'
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('=name',)


class UserViewSet(ModelViewSet):
    lookup_field = 'id'
    queryset = User.objects.all().order_by('-id')
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('=id',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.serializer_class
        elif self.action == "subscriptions":
            return UserSerializer
        else:
            return self.serializer_class
    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated, ],
    )
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        serializer = UserSerializer(
            user, data=request.data,
            partial=True,
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated, ],
    )
    def subscriptions(self, request):
        user = get_object_or_404(User, username=self.request.user)
        follows = Follow.objects.filter(user=user)
        followers = []
        for follow in follows:
            follower = User.objects.get(id=follow.author.id)
            followers.append(follower)
        serializer = self.get_serializer(followers, many=True)

        if request.method == 'PATCH':
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK)
    
    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, ],
        url_path=r'subscribe'
    )
    def subscribe(self, request, id=None):
        user = get_object_or_404(User, username=self.request.user)
        author = get_object_or_404(User, id=id)
        Follow.objects.create(author=author, user=user)
        serializer = UserSerializer(author)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdatePassword(APIView):
    permission_classes = (IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("current_password")
            if not self.object.check_password(old_password):
                return Response({"current_password": ["Wrong password."]}, 
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST', 'get'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    serializer = ConfirmationUserTokenSerializer(data=request.data)
    serializer.is_valid()
    user_obj = get_object_or_404(User,
                                 email="nikox122@mail.ru",
                                 password="456852Zx"
                                 )
    token = AccessToken.for_user(user_obj)
    return Response(
        {'auth_token': str(token)}, status=status.HTTP_200_OK)