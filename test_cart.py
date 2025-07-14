#!/usr/bin/env python
"""
Simple test script for cart functionality
Run with: python test_cart.py
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import RequestFactory
from products.models import Product, Category
from cart.models import Cart, CartItem
from cart.utils import get_or_create_cart
from decimal import Decimal


def test_cart_functionality():
    """Test basic cart functionality"""
    print("🧪 Testing Cart Functionality...")

    # Create a test category and product
    category, created = Category.objects.get_or_create(
        name="Test Category",
        defaults={'description': 'Test category for cart testing'}
    )
    print(f"✅ Category created/found: {category.name}")

    product, created = Product.objects.get_or_create(
        name="Test Product",
        sku="TEST-001",
        defaults={
            'category': category,
            'price': Decimal('19.99'),
            'description': 'Test product for cart testing',
            'is_published': True
        }
    )
    print(f"✅ Product created/found: {product.name} - ${product.price}")

    # Create a mock request with proper session
    from django.contrib.sessions.models import Session
    from django.contrib.sessions.backends.db import SessionStore

    factory = RequestFactory()
    request = factory.get('/')

    # Create a proper session
    session = SessionStore()
    session.create()
    request.session = session
    request.user = User.objects.get_or_create(username='testuser')[0]

    # Test cart creation
    cart = get_or_create_cart(request)
    print(f"✅ Cart created: {cart}")

    # Test adding item to cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 2}
    )

    if not created:
        cart_item.quantity += 2
        cart_item.save()

    print(f"✅ Added {cart_item.quantity}x {product.name} to cart")
    print(f"   Total price: ${cart_item.total_price}")

    # Test cart totals
    print(f"\n📊 Cart Summary:")
    print(f"   Total items: {cart.total_items}")
    print(f"   Total price: ${cart.total_price}")
    print(f"   Is empty: {cart.is_empty()}")

    # Test cart item operations
    original_quantity = cart_item.quantity
    cart_item.increase_quantity(1)
    print(f"✅ Increased quantity: {original_quantity} → {cart_item.quantity}")

    cart_item.decrease_quantity(1)
    print(f"✅ Decreased quantity: {cart_item.quantity + 1} → {cart_item.quantity}")

    # Test clearing cart
    items_before = cart.total_items
    cart.clear()
    print(f"✅ Cart cleared: {items_before} items → {cart.total_items} items")

    print("\n🎉 All cart functionality tests passed!")

    # Cleanup
    CartItem.objects.filter(cart=cart).delete()
    cart.delete()
    product.delete()
    category.delete()
    print("🧹 Cleanup completed")


def test_cart_models():
    """Test cart model properties and methods"""
    print("\n🔍 Testing Cart Models...")

    # Create test data
    category = Category.objects.create(name="Model Test Category")
    product1 = Product.objects.create(
        name="Product 1", sku="MODEL-001", price=Decimal('10.00'),
        category=category, is_published=True
    )
    product2 = Product.objects.create(
        name="Product 2", sku="MODEL-002", price=Decimal('25.50'),
        category=category, is_published=True
    )

    cart = Cart.objects.create()

    # Add items
    item1 = CartItem.objects.create(cart=cart, product=product1, quantity=3)
    item2 = CartItem.objects.create(cart=cart, product=product2, quantity=2)

    # Test calculations
    expected_total_items = 3 + 2  # 5
    expected_total_price = (10.00 * 3) + (25.50 * 2)  # 30.00 + 51.00 = 81.00

    assert cart.total_items == expected_total_items, f"Expected {expected_total_items}, got {cart.total_items}"
    assert cart.total_price == Decimal(str(expected_total_price)), f"Expected {expected_total_price}, got {cart.total_price}"

    print(f"✅ Cart total items: {cart.total_items}")
    print(f"✅ Cart total price: ${cart.total_price}")

    # Test item totals
    assert item1.total_price == Decimal('30.00'), f"Item1 total should be 30.00, got {item1.total_price}"
    assert item2.total_price == Decimal('51.00'), f"Item2 total should be 51.00, got {item2.total_price}"

    print(f"✅ Item 1 total: ${item1.total_price}")
    print(f"✅ Item 2 total: ${item2.total_price}")

    # Cleanup
    cart.delete()
    product1.delete()
    product2.delete()
    category.delete()

    print("✅ Model tests passed!")


if __name__ == '__main__':
    try:
        test_cart_functionality()
        test_cart_models()
        print("\n🎊 All tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
