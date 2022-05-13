import datetime as dt

from django.contrib.auth import get_user_model

from rest_framework import serializers


from reviews.models import Category, Genre, Title, Review, Comment


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Список категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Список жанров"""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleCreateSerializer(serializers.ModelSerializer):
    """Запись произведения."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        many=False,
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        required=False,
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего'
            )
        return value


class TitleListSerializer(serializers.ModelSerializer):
    """Чтение произведений."""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Title


class SignUpSerializer(serializers.ModelSerializer):
    """Регистрация пользователя."""

    class Meta:
        model = User
        fields = ('email', 'username')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя общего назначения."""

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name', 'bio', 'role')


class SafeUserSerializer(serializers.ModelSerializer):
    """Серилазиатор для пользователя с безопасными полями."""

    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name', 'bio', 'role')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор обзоров."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate_score(self, value):
        if value > 10 or value < 1:
            raise serializers.ValidationError(
                'Оценка должна быть от 1 до 10'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment