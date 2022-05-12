from django.urls import include, path

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('users', views.AdminUserViewSet)

urlpatterns = [
    path('v1/auth/signup/', views.SignUp.as_view()),
    path('v1/auth/token/', views.ObtainToken.as_view()),
    path('v1/', include(router.urls)),
]
