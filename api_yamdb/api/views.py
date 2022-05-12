from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import AuthorModerAdmin
from api.serializers import CommentSerializer, ReviewSerializer
from reviews.models import Review, Title

User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    """Обзоры тайтла."""
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [
        AuthorModerAdmin,
    ]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user,
                        title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Комментарии для обзора."""
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [
        AuthorModerAdmin,
    ]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user,
                        review=review)
