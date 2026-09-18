from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Perfume(models.Model):

    GENDER_CHOICES = [
        ('MEN', 'Men'),
        ('WOMEN', 'Women'),
        ('UNISEX', 'Unisex'),
    ]

    CONCENTRATION_CHOICES = [
        ('EDP', 'Eau de Parfum'),
        ('EDT', 'Eau de Toilette'),
        ('EDC', 'Eau de Cologne'),
        ('PARFUM', 'Parfum'),
        ('OIL', 'Perfume Oil'),
    ]

    # Basic information
    name = models.CharField(max_length=255)

    brand = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    # Category
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='perfumes'
    )

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        default='UNISEX'
    )

    # Price
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Perfume details
    size = models.CharField(
        max_length=50,
        default='100ml'
    )

    concentration = models.CharField(
        max_length=20,
        choices=CONCENTRATION_CHOICES,
        default='EDP'
    )

    fragrance_family = models.CharField(
        max_length=100,
        blank=True
    )

    # Fragrance notes
    top_notes = models.TextField(
        blank=True,
        help_text='Example: Bergamot, Lemon, Apple'
    )

    middle_notes = models.TextField(
        blank=True,
        help_text='Example: Lavender, Rose, Jasmine'
    )

    base_notes = models.TextField(
        blank=True,
        help_text='Example: Vanilla, Musk, Cedarwood'
    )

    # Product image
    image = models.ImageField(
        upload_to='perfumes/',
        blank=True,
        null=True
    )

    # Inventory
    stock = models.PositiveIntegerField(default=0)

    # Rating
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0.0
    )

    # Store status
    is_new = models.BooleanField(default=False)

    is_featured = models.BooleanField(default=False)

    is_available = models.BooleanField(default=True)

    # Dates
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.brand} - {self.name}'

    @property
    def current_price(self):

        if self.sale_price is not None:
            return self.sale_price

        return self.price
class Order(models.Model):
    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='orders',
    null=True,
    blank=True,
)

    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('ABA', 'ABA Pay'),
        ('CARD', 'Credit / Debit Card'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    customer_name = models.CharField(max_length=150)

    email = models.EmailField()

    phone = models.CharField(max_length=30)

    address = models.TextField()

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='COD'
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.id} - {self.customer_name}'


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    perfume = models.ForeignKey(
        Perfume,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='order_items'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        perfume_name = (
            self.perfume.name
            if self.perfume
            else 'Deleted perfume'
        )

        return f'{perfume_name} x {self.quantity}'

    @property
    def subtotal(self):
        return self.price * self.quantity