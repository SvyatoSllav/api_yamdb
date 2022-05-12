from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
)

router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]