import base64

from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import serializers

from recipy.models import (Favorite, Ingredient, Recipy, RecipyIngredient,
                           ShoppingCart, Tag)
from users.models import Follow, User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]

            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class MeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "id"]


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=150)
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            ASCIIUsernameValidator(),
        ],
    )
    first_name = serializers.CharField(
        required=True,
        max_length=150,
    )
    last_name = serializers.CharField(
        required=True,
        max_length=150,
    )
    password = serializers.CharField(required=True,
                                     max_length=150,
                                     write_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "id",
            "is_subscribed",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def get_is_subscribed(self, obj):
        if self.context.get("request").method != "POST":
            request = self.context.get("request")
            user = request.user
            return Follow.objects.filter(author=obj, user=user).exists()
        return False

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate(self, data):
        if User.objects.filter(
            username=data["username"],
            email=data["email"]).exists():
            return data
        if User.objects.filter(username=data["username"]):
            raise serializers.ValidationError("такой user уже есть!")
        if User.objects.filter(email=data["email"]):
            raise serializers.ValidationError("Такой email уже есть!")
        return data


class FollowWriteSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        return obj.is_subscribed


class BaseRecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(required=True, many=True)
    author = MeUserSerializer()
    ingredients = serializers.SerializerMethodField()
    name = serializers.CharField(
        required=True,
        max_length=150,
    )
    image = Base64ImageField(required=True, allow_null=True)
    text = serializers.CharField(required=True)
    cooking_time = serializers.IntegerField(required=True)

    class Meta:
        model = Recipy
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_ingredients(self, obj):
        ingredients = obj.ingredients.values()
        for ingredient in ingredients:
            rec_in = RecipyIngredient.objects.get(
                recipy=obj, ingredients=ingredient["id"]
            )
            ingredient["amount"] = rec_in.amount
        return ingredients


class FollowReadSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    username = serializers.CharField(source="author.username")
    email = serializers.CharField(source="author.email")
    first_name = serializers.CharField(source="author.first_name")
    last_name = serializers.CharField(source="author.last_name")

    class Meta:
        model = Follow
        fields = [
            "id",
            "username",
            "is_subscribed",
            "last_name",
            "first_name",
            "email",
            "recipes",
            "recipes_count",
        ]

    def get_recipes(self, obj):
        recipes = Recipy.objects.filter(
            author=obj.author).order_by("-pub_date")
        serializers = BaseRecipeSerializer(recipes, many=True)
        return serializers.data

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, obj):
        return Recipy.objects.filter(author=obj.author).count()


class RecipyFavoriteWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipy
        fields = ("id", "name", "image", "cooking_time")


class RecipyReadSerializer(BaseRecipeSerializer):
    author = UserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipy
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
            "is_favorited",
            "is_in_shopping_cart",
        )

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        user = request.user
        favorited = Favorite.objects.filter(recipy=obj, user=user)
        return favorited.exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        user = request.user
        recipy_in_shopping_cart = ShoppingCart.objects.filter(
            recipy=obj,
            user=user)
        return recipy_in_shopping_cart.exists()


class IngredientWriteRecipySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(write_only=True)


class RecipyWriteSerializer(RecipyReadSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True)
    ingredients = IngredientWriteRecipySerializer(many=True)
    author = UserSerializer(
        required=False,
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        ingredients = instance.ingredients.values()
        for ingredient in ingredients:
            rec_in = RecipyIngredient.objects.get(
                recipy=instance, ingredients=ingredient["id"]
            )
            ingredient["amount"] = rec_in.amount
        representation["ingredients"] = ingredients
        return representation

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipy = Recipy.objects.create(**validated_data)
        recipy.tags.set(tags)
        RecipyIngredient.objects.bulk_create(
            [
                RecipyIngredient(
                    ingredients=Ingredient(ingredient["id"]),
                    recipy=recipy,
                    amount=ingredient["amount"],
                )
                for ingredient in ingredients
            ]
        )
        return recipy

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        instance.tags.set(tags)
        RecipyIngredient.objects.filter(
            recipy=instance,
        ).delete()
        RecipyIngredient.objects.bulk_create(
            [
                RecipyIngredient(
                    ingredients=Ingredient(ingredient["id"]),
                    recipy=instance,
                    amount=ingredient["amount"],
                )
                for ingredient in ingredients
            ]
        )
        return instance
