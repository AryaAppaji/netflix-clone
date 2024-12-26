"""
URL configuration for netflix clone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
)
from users.views.authentication_view import (
    LoginView,
    LogoutView,
)
from users.views.user_view import UserViewSet
from movies.views.genre_view import GenreViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="users")
router.register(r"genre", GenreViewSet, basename="genre")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("silk/", include("silk.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/login", LoginView.as_view(), name="login"),
    path("api/logout", LogoutView.as_view(), name="logout"),
    path("api/", include(router.urls)),
]
