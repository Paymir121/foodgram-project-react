from django.contrib.auth.validators import ASCIIUsernameValidator
from rest_framework import serializers
from users.models import User, Follow
from recipy.models import Tag, Recipy, Ingredient, RecipyIngredient, Favorite, ShoppingCart
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404 
from django.contrib.auth.password_validation import validate_password
import base64
from django.core.files.base import ContentFile
from rest_framework import filters, mixins, status
from rest_framework.response import Response
from djoser.serializers import UserSerializer

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class MeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'id']


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=150)
    username = serializers.CharField(required=True,
                                     max_length=150,
                                     validators=[ASCIIUsernameValidator(),])
    first_name = serializers.CharField(required=True, max_length=150,)
    last_name = serializers.CharField(required=True, max_length=150,)
    password = serializers.CharField(required=True, max_length=150, write_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email',
                  'username',
                  'password',
                  'first_name',
                  'last_name',
                  'id',
                  'is_subscribed']
        extra_kwargs = {'password': {'write_only': True}}

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        followed = Follow.objects.filter(author=obj, user=user)
        return followed.exists()
    
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        if User.objects.filter(username=data['username'],
                               email=data['email']).exists():
            return data
        if User.objects.filter(username=data['username']):
            raise serializers.ValidationError('такой user уже есть!')
        if User.objects.filter(email=data['email']):
            raise serializers.ValidationError('Такой email уже есть!')
        return data


class FavoriteWriteSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        return obj.is_subscribed


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientWriteRecipySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()


class RecipyReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(required=True, many=True)
    author = UserSerializer()
    ingredients = serializers.SerializerMethodField()
    name = serializers.CharField(required=True, max_length=150,)
    image = Base64ImageField(required=True, allow_null=True)
    text = serializers.CharField(required=True)
    cooking_time = serializers.IntegerField(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipy
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'name',
                  'image',
                  'text',
                  'cooking_time',
                  "is_favorited",
                  "is_in_shopping_cart",
                  )
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user = request.user
        favorited = Favorite.objects.filter(recipy=obj, user=user)
        return favorited.exists()
        
    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        user = request.user
        recipy_in_shopping_cart = ShoppingCart.objects.filter(recipy=obj, user=user)
        return recipy_in_shopping_cart.exists()
    
    def get_ingredients(self, obj):
        ingredients = obj.ingredients.values()
        for ingredient in ingredients:
            amount = RecipyIngredient.objects.get(recipy=obj, ingredients=ingredient['id']).amount
            ingredient['amount'] = amount
        return ingredients


class RecipyWriteSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = IngredientWriteRecipySerializer(many=True)
    name = serializers.CharField(required=True, max_length=150,)
    image = Base64ImageField(required=False, allow_null=True)
    text = serializers.CharField(required=True)
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipy
        fields = ('id',
                  'tags',
                  'ingredients',
                  'name',
                  'image',
                  'text',
                  'cooking_time',
                  )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipy = Recipy.objects.create(**validated_data)
        recipy.tags.set(tags)
        for ingredient in ingredients:
            amount = ingredient.pop('amount')
            current_ingredient = Ingredient.objects.get(id=ingredient['id'])
            RecipyIngredient.objects.create(
                ingredients=current_ingredient,
                recipy=recipy,
                amount=amount
            )
        return recipy

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        for ingredient in ingredients:
            amount = ingredient.pop('amount')
            current_ingredient = Ingredient.objects.get(id=ingredient['id'])
            RecipyIngredient.objects.update_or_create(
                ingredients=current_ingredient,
                recipy=instance,
            )

            ingredient_in_recipy = RecipyIngredient.objects.get(
                ingredients=current_ingredient,
                recipy=instance,)
            ingredient_in_recipy.amount = amount
            ingredient_in_recipy.save()
        return super().update(instance, validated_data)
    

class RecipyFavoriteWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipy
        fields = ('id', 'name', 'image', 'cooking_time')