import uuid

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User

from .utils import send_mail
from .permissions import (IsAdmin,)
from .serializers import (ConfirmationCodeSerializer,
                          RegistrationSerializer,
                          UserSerializer)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = str(uuid.uuid4())
        user, _ = User.objects.get_or_create(
            email=serializer.validated_data['email'],
            username=serializer.validated_data['username'],)
        send_mail(user.email, confirmation_code)
        user.confirmation_code = confirmation_code
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all().order_by('-id')
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('=username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[AllowAny, ],
    )
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        serializer = UserSerializer(
            user, data=request.data,
            partial=True,
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user_obj = get_object_or_404(User,
                                 username=serializer.validated_data['username']
                                 )
    token = AccessToken.for_user(user_obj)
    return Response(
        {'token': str(token)}, status=status.HTTP_200_OK)