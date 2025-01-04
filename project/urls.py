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
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from users.views.authentication_view import (
    LoginView,
    LogoutView,
)
from users.views.user_view import UserViewSet
from movies.views.genre_view import GenreViewSet
from movies.views.movie_view import MovieViewSet
from movies.views.movie_review_view import MovieReviewViewSet
from finance.views.subscription_view import SubscriptionViewSet
from finance.views.payment_mode_view import PaymentModeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="users")
router.register(r"genre", GenreViewSet, basename="genres")
router.register(r"subscription", SubscriptionViewSet, basename="subscriptions")
router.register(r"payment-mode", PaymentModeViewSet, basename="payment_modes")
router.register(r"movie", MovieViewSet, basename="movies")
router.register(r"review", MovieReviewViewSet, basename="movie_reviews")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sonar/", include("django_sonar.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path("api/login", LoginView.as_view(), name="login"),
    path("api/logout", LogoutView.as_view(), name="logout"),
    path("api/", include(router.urls)),
]
