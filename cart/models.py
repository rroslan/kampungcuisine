from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from products.models import Product


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='carts'
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        if self.session_key:
            return f"Anonymous Cart ({self.session_key[:8]}...)"
        return "Anonymous Cart (no session)"

    @property
    def total_items(self):
        """Return total number of items in cart."""
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        """Return total price of all items in cart."""
        return sum(item.total_price for item in self.items.all())

    def clear(self):
        """Remove all items from cart."""
        self.items.all().delete()

    def is_empty(self):
        """Check if cart is empty."""
        return not self.items.exists()


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'product')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def total_price(self):
        """Return total price for this cart item."""
        return self.product.price * self.quantity

    def increase_quantity(self, amount=1):
        """Increase quantity by specified amount."""
        self.quantity += amount
        self.save()

    def decrease_quantity(self, amount=1):
        """Decrease quantity by specified amount."""
        if self.quantity > amount:
            self.quantity -= amount
            self.save()
        else:
            self.delete()
