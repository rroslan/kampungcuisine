from django.db import models
from django.utils.text import slugify
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    sku = models.CharField(
        max_length=50,
        unique=True,
        help_text="Stock Keeping Unit"
    )
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    is_published = models.BooleanField(default=False)

    # Image fields
    image_main = models.ImageField(
        upload_to='products/main/',
        blank=True,
        null=True,
        help_text="Main product image"
    )
    image_1 = models.ImageField(
        upload_to='products/additional/',
        blank=True,
        null=True,
        help_text="Additional product image 1"
    )
    image_2 = models.ImageField(
        upload_to='products/additional/',
        blank=True,
        null=True,
        help_text="Additional product image 2"
    )
    image_3 = models.ImageField(
        upload_to='products/additional/',
        blank=True,
        null=True,
        help_text="Additional product image 3"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['is_published']),
            models.Index(fields=['-created_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def get_all_images(self):
        """Return a list of all non-null images."""
        images = []
        if self.image_main:
            images.append(self.image_main)
        if self.image_1:
            images.append(self.image_1)
        if self.image_2:
            images.append(self.image_2)
        if self.image_3:
            images.append(self.image_3)
        return images

    @property
    def is_available(self):
        """Check if product is available (published)."""
        return self.is_published
