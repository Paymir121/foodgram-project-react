from django.contrib.auth.validators import ASCIIUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from users.models import User
from users.validators import validator_username


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=150)
    username = serializers.CharField(required=True,
                                     max_length=150,
                                     validators=[ASCIIUsernameValidator(),
                                                 validator_username])

    class Meta:
        fields = ['email', 'username', ]

    def validate(self, data):
        if User.objects.filter(username=data['username'],
                               email=data['email']).exists():
            return data
        if User.objects.filter(username=data['username']):
            raise serializers.ValidationError('такой user уже есть!')
        if User.objects.filter(email=data['email']):
            raise serializers.ValidationError('Такой email уже есть!')
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email',
                  'username',
                  'first_name',
                  'last_name',
                  'role',
                  'bio'
                  ]

    def validate(self, data):
        if 'username' in data:
            if User.objects.filter(username=data['username']):
                raise serializers.ValidationError('такой user уже есть!')
        if 'email' in data:
            if User.objects.filter(email=data['email']):
                raise serializers.ValidationError(
                    'Такой email уже есть!')
        return data


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, attrs):
        user_obj = get_object_or_404(User, username=attrs["username"])
        if user_obj.confirmation_code != attrs["confirmation_code"]:
            raise serializers.ValidationError({
                "confirmation_code": "Неправильный код!"})
        return attrs
