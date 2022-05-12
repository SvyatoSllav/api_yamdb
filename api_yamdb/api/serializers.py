from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name', 'bio', 'role')


class SafeUserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name', 'bio', 'role')
