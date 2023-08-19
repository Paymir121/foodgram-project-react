import csv

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from users.models import Follow, User
from recipy.models import Favorite, Ingredient, Recipy, ShoppingCart, Tag

from .filters import RecipyFilter
from .permissions import IsAdminOrReadOnly, IsAuthenticatednOrReadOnly
from .serializers import (BaseRecipeSerializer, FollowReadSerializer,
                          FollowWriteSerializer, IngredientSerializer,
                          MeUserSerializer, RecipyFavoriteWriteSerializer,
                          RecipyIngredient, RecipyReadSerializer,
                          RecipyWriteSerializer, TagSerializer, UserSerializer)


class TagViewSet(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
    lookup_field = "id"
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipyViewSet(ModelViewSet):
    serializer_class = BaseRecipeSerializer
    permission_classes = (IsAuthenticatednOrReadOnly,)
    queryset = Recipy.objects.order_by("-pub_date")
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipyFilter
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            if self.request.user.is_authenticated:
                return RecipyReadSerializer
            else:
                return BaseRecipeSerializer
        return RecipyWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Recipy.objects.all()
        is_favorited = self.request.query_params.get("is_favorited")
        author = self.request.query_params.get("author")
        is_in_cart = self.request.query_params.get("is_in_shopping_cart")
        user = self.request.user
        if is_favorited:
            queryset = Recipy.objects.filter(favorites__user=user)
        if author:
            queryset = Recipy.objects.filter(author=author)
        if is_in_cart:
            queryset = Recipy.objects.filter(purchase__user=user)
        return queryset

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[
            IsAuthenticated,
        ],
        url_path=r"favorite",
    )
    def favorite(self, request, pk=None):
        user = get_object_or_404(User, username=self.request.user)
        recipy = get_object_or_404(Recipy, id=pk)
        if request.method == "DELETE":
            Favorite.objects.filter(recipy=recipy, user=user).delete()
            return Response({"errors": recipy.name}, status=status.HTTP_200_OK)
        if request.method == "POST":
            Favorite.objects.get_or_create(recipy=recipy, user=user)
            serializer = RecipyFavoriteWriteSerializer(recipy)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[
            IsAuthenticated,
        ],
        url_path=r"shopping_cart",
    )
    def shopping_cart(self, request, pk=None):
        user = get_object_or_404(User, username=self.request.user)
        recipy = get_object_or_404(Recipy, id=pk)
        if request.method == "DELETE":
            ShoppingCart.objects.filter(recipy=recipy, user=user).delete()
        if request.method == "POST":
            ShoppingCart.objects.create(recipy=recipy, user=user)
        serializer = RecipyFavoriteWriteSerializer(recipy)
        # Убрать нельзя, так как по Redoc должен быть ответ
        # в виде названия рецепта и времени готовки
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=[
            "get",
        ],
        permission_classes=[
            IsAuthenticated,
        ],
        url_path=r"download_shopping_cart",
    )
    def download_shopping_cart(self, request):
        user = get_object_or_404(User, username=self.request.user)
        shoping_carts = ShoppingCart.objects.filter(user=user)
        ingredients_in_cart = dict()
        headers_key = "Content-Disposition"
        headers_value = 'attachment; filename="somefilename.csv"'
        headers = {headers_key: headers_value}
        response = HttpResponse(
            content_type="text/csv",
            headers=headers,
        )
        writer = csv.writer(response)
        for shoping_cart in shoping_carts:
            ingredients_in_recipy = RecipyIngredient.objects.filter(
                recipy=shoping_cart.recipy
            )
            for ingredients in ingredients_in_recipy:
                name = ingredients.ingredients.name
                amount = ingredients.amount
                measurement_unit = ingredients.ingredients.measurement_unit

                if name not in ingredients_in_cart:
                    ingredients_in_cart[name] = {
                        "amount": amount,
                        "measurement_unit": measurement_unit,
                    }
                else:
                    ingredients_in_cart[name]["amount"] += amount
        for name in ingredients_in_cart:
            ingredient = ingredients_in_cart[name]
            amount = ingredient["amount"]
            measurement_unit = ingredient["measurement_unit"]
            writer.writerow([name, amount, measurement_unit])
        return response


class IngredientViewSet(ModelViewSet):
    lookup_field = "id"
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class UserViewSet(ModelViewSet):
    lookup_field = "id"
    queryset = User.objects.all().order_by("-id")
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("=id",)
    http_method_names = ["get", "post", "patch", "delete"]
    pagination_class = LimitOffsetPagination

    @action(
        detail=False,
        methods=[
            "get",
        ],
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def me(self, request):
        user = get_object_or_404(User, username=request.user)
        serializer = MeUserSerializer(
            user, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[
            IsAuthenticated,
        ],
        url_path=r"subscribe",
    )
    def subscribe(self, request, id=None):
        user = get_object_or_404(User, username=self.request.user)
        author = get_object_or_404(User, id=id)
        if request.method == "DELETE":
            Follow.objects.filter(author=author, user=user).delete()
            author.is_subscribed = False
        if request.method == "POST":
            Follow.objects.get_or_create(author=author, user=user)
            author.is_subscribed = True
        serializer = FollowWriteSerializer(author)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIFollow(APIView, LimitOffsetPagination):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        user_follower = Follow.objects.filter(user=request.user)
        serializer = FollowReadSerializer(
            user_follower,
            many=True,
        )
        queryset = self.paginate_queryset(serializer.data, request)
        return self.get_paginated_response(queryset)


class APISet_Password(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        user = request.user
        old_password = request.data["current_password"]
        new_password = request.data["new_password"]
        if user.check_password(old_password):
            user.set_password(new_password)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            context = {"error": "Гуляй лесом, неправильный пароль"}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
