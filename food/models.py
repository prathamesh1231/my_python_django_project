from django.db import models
from django.contrib.auth.models import User


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('pizza',   'Pizza'),
        ('burger',  'Burger'),
        ('snack',   'Snack'),
        ('drink',   'Drink'),
    ]
    name        = models.CharField(max_length=100)
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    image       = models.CharField(max_length=200)
    emoji       = models.CharField(max_length=10, default='🍽️')
    description = models.TextField(blank=True)
    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='snack')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name       = models.CharField(max_length=100)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%d %b %Y')}"


class Cart(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def item_count(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart      = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity  = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',    'Pending'),
        ('confirmed',  'Confirmed'),
        ('preparing',  'Preparing'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
    ]
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total      = models.DecimalField(max_digits=10, decimal_places=2)
    address    = models.TextField()
    phone      = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order     = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity  = models.PositiveIntegerField()
    price     = models.DecimalField(max_digits=8, decimal_places=2)  # price at time of order

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"
