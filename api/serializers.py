from rest_framework import serializers

from .models import Category, Perfume, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category.
    """

    class Meta:
        model = Category

        fields = [
            'id',
            'name',
            'description',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
        ]


class PerfumeSerializer(serializers.ModelSerializer):
    """
    Serializer for Perfume.
    """

    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )

    current_price = serializers.ReadOnlyField()

    class Meta:
        model = Perfume

        fields = [
            'id',

            'name',
            'brand',
            'description',

            'category',
            'category_name',
            'gender',

            'price',
            'sale_price',
            'current_price',

            'size',
            'concentration',
            'fragrance_family',

            'top_notes',
            'middle_notes',
            'base_notes',

            'image',

            'stock',

            'rating',

            'is_new',
            'is_featured',
            'is_available',

            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'category_name',
            'current_price',
            'created_at',
            'updated_at',
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for an individual order item.
    """

    perfume_name = serializers.CharField(
        source='perfume.name',
        read_only=True
    )

    perfume_brand = serializers.CharField(
        source='perfume.brand',
        read_only=True
    )

    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem

        fields = [
            'id',
            'perfume',
            'perfume_name',
            'perfume_brand',
            'price',
            'quantity',
            'subtotal',
        ]

        read_only_fields = [
            'id',
            'perfume_name',
            'perfume_brand',
            'subtotal',
        ]


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for an Order and its OrderItems.
    """

    items = OrderItemSerializer(
        many=True
    )

    class Meta:
        model = Order

        fields = [
            'id',
            'customer_name',
            'email',
            'phone',
            'address',
            'payment_method',
            'total',
            'status',
            'items',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'status',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        items_data = validated_data.pop(
            'items',
            []
        )

        order = Order.objects.create(
            **validated_data
        )

        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                **item_data
            )

        return order