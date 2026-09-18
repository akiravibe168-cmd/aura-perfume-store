from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    CategoryViewSet,
    PerfumeViewSet,
    OrderCreateView,
    OrderDetailView,
    MyOrdersView,
    RegisterView,
    MeView,
)


router = DefaultRouter()

router.register(
    r"categories",
    CategoryViewSet,
    basename="category",
)

router.register(
    r"perfumes",
    PerfumeViewSet,
    basename="perfume",
)


urlpatterns = [
    # Products
    path(
        "",
        include(router.urls),
    ),

    # Orders
    path(
        "orders/",
        OrderCreateView.as_view(),
        name="order-create",
    ),

    path(
        "orders/<int:pk>/",
        OrderDetailView.as_view(),
        name="order-detail",
    ),

    path(
        "my-orders/",
        MyOrdersView.as_view(),
        name="my-orders",
    ),

    # Authentication
    path(
        "auth/register/",
        RegisterView.as_view(),
        name="register",
    ),

    path(
        "auth/login/",
        TokenObtainPairView.as_view(),
        name="login",
    ),

    path(
        "auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),

    path(
        "auth/me/",
        MeView.as_view(),
        name="me",
    ),
]