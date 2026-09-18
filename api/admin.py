from django.contrib import admin
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Category, Perfume, Order, OrderItem


# =========================================================
# CATEGORY
# =========================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "created_at",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )

    list_per_page = 20


# =========================================================
# PERFUME / PRODUCTS
# =========================================================

@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):

    list_display = (
        "product_name",
        "brand_name",
        "price_display",
        "stock_display",
        "rating_display",
        "status_display",
    )

    list_display_links = (
        "product_name",
    )

    list_filter = (
        "brand",
        "category",
        "gender",
        "concentration",
        "is_new",
        "is_featured",
        "is_available",
    )

    search_fields = (
        "name",
        "brand",
        "description",
        "fragrance_family",
        "top_notes",
        "middle_notes",
        "base_notes",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "image_preview_large",
    )

    list_per_page = 20

    # -----------------------------------------------------
    # CUSTOM PRODUCT STATUS FILTER
    # -----------------------------------------------------

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        stock_status = request.GET.get("stock_status")

        if stock_status == "active":
            queryset = queryset.filter(
                is_available=True,
                stock__gt=5,
            )

        elif stock_status == "low":
            queryset = queryset.filter(
                is_available=True,
                stock__gt=0,
                stock__lte=5,
            )

        elif stock_status == "out":
            queryset = queryset.filter(
                stock__lte=0,
            )

        return queryset

    # -----------------------------------------------------
    # EDIT PAGE
    # -----------------------------------------------------

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "brand",
                    "description",
                    "category",
                    "gender",
                )
            },
        ),
        (
            "Price & Inventory",
            {
                "fields": (
                    "price",
                    "sale_price",
                    "stock",
                )
            },
        ),
        (
            "Perfume Details",
            {
                "fields": (
                    "size",
                    "concentration",
                    "fragrance_family",
                )
            },
        ),
        (
            "Fragrance Notes",
            {
                "fields": (
                    "top_notes",
                    "middle_notes",
                    "base_notes",
                )
            },
        ),
        (
            "Product Image",
            {
                "fields": (
                    "image",
                    "image_preview_large",
                )
            },
        ),
        (
            "Store Status",
            {
                "fields": (
                    "rating",
                    "is_new",
                    "is_featured",
                    "is_available",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    # -----------------------------------------------------
    # PRODUCT NAME
    # -----------------------------------------------------

    @admin.display(description="Product")
    def product_name(self, obj):

        if obj.image:
            image_html = format_html(
                '<img src="{}" class="aura-product-image" alt="{}">',
                obj.image.url,
                obj.name,
            )
        else:
            image_html = mark_safe(
                '<div class="aura-product-image aura-product-image-empty">'
                '<span>NO IMAGE</span>'
                '</div>'
            )

        category_name = (
            obj.category.name
            if obj.category
            else "Uncategorized"
        )

        edit_url = reverse(
            "admin:api_perfume_change",
            args=[obj.pk],
        )

        return format_html(
            """
            <div class="aura-product-cell">

                <div class="aura-product-photo">
                    {}
                </div>

                <div class="aura-product-copy">
                    <a href="{}" class="aura-product-title">
                        {}
                    </a>

                    <span class="aura-product-category">
                        {}
                    </span>
                </div>

            </div>
            """,
            image_html,
            edit_url,
            obj.name,
            category_name,
        )

    # -----------------------------------------------------
    # BRAND
    # -----------------------------------------------------

    @admin.display(description="Brand")
    def brand_name(self, obj):

        return format_html(
            """
            <span class="aura-brand">
                {}
            </span>
            """,
            obj.brand or "—",
        )

    # -----------------------------------------------------
    # PRICE
    # -----------------------------------------------------

    @admin.display(description="Price")
    def price_display(self, obj):

        if obj.sale_price:

            return format_html(
                """
                <div class="aura-price-wrap">

                    <strong class="aura-price-sale">
                        ${}
                    </strong>

                    <span class="aura-price-old">
                        ${}
                    </span>

                </div>
                """,
                obj.sale_price,
                obj.price,
            )

        return format_html(
            """
            <strong class="aura-price-normal">
                ${}
            </strong>
            """,
            obj.price,
        )

    # -----------------------------------------------------
    # STOCK
    # -----------------------------------------------------

    @admin.display(description="Stock")
    def stock_display(self, obj):

        if obj.stock <= 0:

            return mark_safe(
                """
                <div class="aura-stock aura-stock-out">
                    <span class="aura-stock-dot"></span>
                    Out of stock
                </div>
                """
            )

        if obj.stock <= 5:

            return format_html(
                """
                <div class="aura-stock aura-stock-low">
                    <span class="aura-stock-dot"></span>
                    {} left
                </div>
                """,
                obj.stock,
            )

        return format_html(
            """
            <div class="aura-stock aura-stock-good">
                <span class="aura-stock-dot"></span>
                {} in stock
            </div>
            """,
            obj.stock,
        )

    # -----------------------------------------------------
    # RATING
    # -----------------------------------------------------

    @admin.display(description="Rating")
    def rating_display(self, obj):

        return format_html(
            """
            <div class="aura-rating">

                <span class="aura-star">
                    ★
                </span>

                <strong>
                    {}
                </strong>

            </div>
            """,
            obj.rating,
        )

    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    @admin.display(description="Status")
    def status_display(self, obj):

        if not obj.is_available:

            return mark_safe(
                """
                <span class="aura-status aura-status-off">
                    Unavailable
                </span>
                """
            )

        if obj.stock <= 0:

            return mark_safe(
                """
                <span class="aura-status aura-status-out">
                    Out of stock
                </span>
                """
            )

        if obj.stock <= 5:

            return mark_safe(
                """
                <span class="aura-status aura-status-low">
                    Low stock
                </span>
                """
            )

        return mark_safe(
            """
            <span class="aura-status aura-status-live">
                Active
            </span>
            """
        )

    # -----------------------------------------------------
    # LARGE IMAGE PREVIEW
    # -----------------------------------------------------

    @admin.display(description="Preview")
    def image_preview_large(self, obj):

        if obj.image:

            return format_html(
                """
                <div class="aura-large-product-image">
                    <img src="{}" alt="{}">
                </div>
                """,
                obj.image.url,
                obj.name,
            )

        return mark_safe(
            """
            <div class="aura-large-product-empty">
                No product image
            </div>
            """
        )


# =========================================================
# ORDER ITEM INLINE
# =========================================================

class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0

    fields = (
        "perfume",
        "price",
        "quantity",
        "item_subtotal",
    )

    readonly_fields = (
        "item_subtotal",
    )

    @admin.display(description="Subtotal")
    def item_subtotal(self, obj):

        if obj.pk:
            return obj.subtotal

        return "-"


# =========================================================
# ORDER
# =========================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "customer_name",
        "email",
        "phone",
        "payment_method",
        "total",
        "status",
        "created_at",
    )

    list_display_links = (
        "id",
        "customer_name",
    )

    list_filter = (
        "status",
        "payment_method",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "customer_name",
        "email",
        "phone",
        "address",
    )

    ordering = (
        "-created_at",
    )

    list_editable = (
        "status",
    )

    readonly_fields = (
        "user",
        "created_at",
        "updated_at",
    )

    inlines = (
        OrderItemInline,
    )

    fieldsets = (
        (
            "Account",
            {
                "fields": (
                    "user",
                )
            },
        ),
        (
            "Customer Information",
            {
                "fields": (
                    "customer_name",
                    "email",
                    "phone",
                    "address",
                )
            },
        ),
        (
            "Order Information",
            {
                "fields": (
                    "payment_method",
                    "status",
                    "total",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    list_per_page = 20


# =========================================================
# ORDER ITEM
# =========================================================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "perfume",
        "price",
        "quantity",
        "item_subtotal",
    )

    list_filter = (
        "order",
        "perfume",
    )

    search_fields = (
        "perfume__name",
        "perfume__brand",
        "order__customer_name",
        "order__email",
        "order__user__username",
        "order__user__email",
    )

    @admin.display(description="Subtotal")
    def item_subtotal(self, obj):
        return obj.subtotal