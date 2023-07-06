from django.contrib.auth.validators import ASCIIUsernameValidator
from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from django.shortcuts import get_object_or_404 
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=150)
    username = serializers.CharField(required=True,
                                     max_length=150,
                                     validators=[ASCIIUsernameValidator(),])
    first_name = serializers.CharField(required=True, max_length=150,)
    last_name = serializers.CharField(required=True, max_length=150,)
    password = serializers.CharField(required=True, max_length=150, write_only=True)
    # id = 

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'id']

    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    def validate(self, data):
        if User.objects.filter(username=data['username'],
                               email=data['email']).exists():
            return data
        if User.objects.filter(username=data['username']):
            raise serializers.ValidationError('такой user уже есть!')
        if User.objects.filter(email=data['email']):
            raise serializers.ValidationError('Такой email уже есть!')
        return data


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
  
class MyTokenObtainPairSerializer(TokenObtainPairSerializer): 

    def validate(self, attrs): 
        self.user = get_object_or_404(User, username=attrs["username"]) 
        if self.user.password == attrs["password"]: 
            token = self.get_token(self.user) 
            access_token = str(token.access_token) 
            return {'access token': access_token, 

                    } 
        raise serializers.ValidationError('неправильный password!') 