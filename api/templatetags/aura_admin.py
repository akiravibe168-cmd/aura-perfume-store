from datetime import timedelta

from django import template
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone

from api.models import Perfume, Category, Order


register = template.Library()


@register.simple_tag
def get_dashboard_stats():

    # =========================================================
    # BASIC COUNTS
    # =========================================================

    products_count = Perfume.objects.count()

    categories_count = Category.objects.count()

    orders_count = Order.objects.count()

    customers_count = User.objects.filter(
        is_staff=False
    ).count()


    # =========================================================
    # REVENUE
    # Cancelled orders are excluded
    # =========================================================

    revenue = (
        Order.objects
        .exclude(status="CANCELLED")
        .aggregate(total=Sum("total"))
        .get("total")
        or 0
    )


    # =========================================================
    # ORDER STATUS
    # =========================================================

    pending_orders = Order.objects.filter(
        status="PENDING"
    ).count()

    processing_orders = Order.objects.filter(
        status="PROCESSING"
    ).count()

    shipped_orders = Order.objects.filter(
        status="SHIPPED"
    ).count()

    delivered_orders = Order.objects.filter(
        status="DELIVERED"
    ).count()


    # =========================================================
    # LOW STOCK
    # =========================================================

    low_stock_products = (
        Perfume.objects
        .filter(
            is_available=True,
            stock__lte=5
        )
        .order_by("stock", "name")[:5]
    )


    # =========================================================
    # RECENT ORDERS
    # =========================================================

    recent_orders = (
        Order.objects
        .select_related("user")
        .order_by("-created_at")[:6]
    )


    # =========================================================
    # SALES - LAST 7 DAYS
    # =========================================================

    today = timezone.localdate()

    sales_chart = []

    for i in range(6, -1, -1):

        date = today - timedelta(days=i)

        amount = (
            Order.objects
            .filter(
                created_at__date=date
            )
            .exclude(
                status="CANCELLED"
            )
            .aggregate(
                total=Sum("total")
            )
            .get("total")
            or 0
        )

        sales_chart.append({
            "label": date.strftime("%a"),
            "amount": float(amount),
            "date": date,
        })


    # =========================================================
    # CHART LEVEL
    # =========================================================

    max_amount = max(
        [day["amount"] for day in sales_chart],
        default=0
    )

    for day in sales_chart:

        if max_amount <= 0:

            day["level"] = 1

        else:

            percentage = (
                day["amount"] / max_amount
            ) * 100

            level = round(
                percentage / 10
            )

            level = max(
                1,
                min(10, level)
            )

            day["level"] = level


    # =========================================================
    # RETURN DATA
    # =========================================================

    return {

        "products": products_count,

        "categories": categories_count,

        "orders": orders_count,

        "customers": customers_count,

        "revenue": revenue,

        "pending_orders": pending_orders,

        "processing_orders": processing_orders,

        "shipped_orders": shipped_orders,

        "delivered_orders": delivered_orders,

        "low_stock": low_stock_products,

        "recent_orders": recent_orders,

        "sales_chart": sales_chart,

    }