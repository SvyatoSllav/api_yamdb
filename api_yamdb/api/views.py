from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignUpSerializer, UserSerializer, SafeUserSerializer

from users.permissions import UserPermissions


User = get_user_model()


class SignUp(APIView):

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(password='', confirmation_code='')

            username = request.data.get('username')
            email = request.data.get('email')
            user = get_object_or_404(User, username=username, email=email)
            confirmation_code = default_token_generator.make_token(user)
            user.password = confirmation_code
            user.confirmation_code = confirmation_code
            user.save()

            send_mail(
                'Код подтверждения',
                confirmation_code,
                settings.EMAIL_HOST_USER,
                [email]
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)


class ObtainToken(APIView):

    def post(self, request):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        try:
            user = User.objects.get(
                username=username,
                confirmation_code=confirmation_code
            )
            refresh = RefreshToken.for_user(user)
            return Response({'access_token': str(refresh.access_token)})

        except ObjectDoesNotExist:
            return Response('User does not exists')


class AdminUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter, )
    search_fields = ('username', )
    permission_classes = (UserPermissions, )
    lookup_field = 'username'
    PageNumberPagination.page_size = 10
    pagination_class = PageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        if kwargs['username'] != 'me':
            return super(
                AdminUserViewSet, self).retrieve(request, *args, **kwargs)

        user = get_object_or_404(User, username=request.user.username)
        user_fields = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': user.bio,
            'role': user.role,
        }
        return Response(user_fields)

    def partial_update(self, request, *args, **kwargs):
        if kwargs['username'] != 'me':
            return super(
                AdminUserViewSet, self
            ).partial_update(request, *args, **kwargs)

        user = get_object_or_404(User, username=request.user.username)
        serializer = SafeUserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def destroy(self, request, *args, **kwargs):
        if kwargs['username'] != 'me':
            return super().destroy(request, *args, **kwargs)
        return Response('Method not allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)

