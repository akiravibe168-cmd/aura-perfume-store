from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Perfume, Order
from .serializers import (
    CategorySerializer,
    PerfumeSerializer,
    OrderSerializer,
)

from .auth_serializers import (
    RegisterSerializer,
    UserSerializer,
)


# ============================================================
# CATEGORY
# ============================================================

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


# ============================================================
# PERFUME
# ============================================================

class PerfumeViewSet(viewsets.ModelViewSet):
    queryset = Perfume.objects.select_related(
        "category"
    ).all()

    serializer_class = PerfumeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Perfume.objects
            .select_related("category")
            .all()
            .order_by("-created_at")
        )


# ============================================================
# CREATE ORDER
# ============================================================

class OrderCreateView(APIView):
    """
    Create an order for the logged-in user.

    POST /api/orders/
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(
            data=request.data
        )

        if serializer.is_valid():
            order = serializer.save(
                user=request.user
            )

            return Response(
                {
                    "success": True,
                    "message": "Order created successfully.",
                    "order": OrderSerializer(order).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# ============================================================
# ORDER DETAIL
# ============================================================

class OrderDetailView(RetrieveAPIView):
    """
    Get one order.

    GET /api/orders/<id>/
    """

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .prefetch_related("items__perfume")
        )


# ============================================================
# MY ORDERS
# ============================================================

class MyOrdersView(APIView):
    """
    Get orders belonging to the logged-in user.

    GET /api/my-orders/
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        orders = (
            Order.objects
            .filter(user=request.user)
            .prefetch_related("items__perfume")
            .order_by("-created_at")
        )

        serializer = OrderSerializer(
            orders,
            many=True
        )

        return Response(
            {
                "success": True,
                "orders": serializer.data,
            }
        )


# ============================================================
# REGISTER
# ============================================================

class RegisterView(APIView):
    """
    Register a new AURA customer.

    POST /api/auth/register/
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "success": True,
                "message": "Registration successful.",
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# CURRENT USER
# ============================================================

class MeView(APIView):
    """
    Get the currently logged-in user.

    GET /api/auth/me/
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "success": True,
                "user": UserSerializer(
                    request.user
                ).data,
            }
        )