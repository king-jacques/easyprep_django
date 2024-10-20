from . import views
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = routers.DefaultRouter()
router.register(r'', views.UserView, 'user')

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("jwt/create/", TokenObtainPairView.as_view(), name="jwt_create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("home", views.homepage_view, name="homepage_view"),
    path("sign-up/", views.signup_view, name="signup_view"),
    path("log-in/", views.login_view, name="login_view"),
    path("", include(router.urls))
]
