#!/usr/bin/env python
"""
Cart Functionality Debug Script
This script helps diagnose cart-related issues step by step
"""

import os
import sys
import django
from django.conf import settings

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.test import RequestFactory, Client
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.urls import reverse
from products.models import Product, Category
from cart.models import Cart, CartItem
from cart.utils import get_or_create_cart
from decimal import Decimal
import json


def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def print_step(step, description):
    """Print a formatted step"""
    print(f"\n🔍 Step {step}: {description}")
    print("-" * 40)


def create_test_data():
    """Create test category and products"""
    print_header("CREATING TEST DATA")

    # Create category
    category, created = Category.objects.get_or_create(
        name="Debug Test Category",
        defaults={'description': 'Category for debugging cart functionality'}
    )

    print(f"✅ Category: {category.name} ({'created' if created else 'existing'})")

    # Create products
    products = []
    for i in range(1, 4):
        product, created = Product.objects.get_or_create(
            name=f"Debug Product {i}",
            sku=f"DEBUG-00{i}",
            defaults={
                'category': category,
                'price': Decimal(f'{10 + i}.99'),
                'description': f'Debug product {i} for cart testing',
                'is_published': True
            }
        )
        products.append(product)
        print(f"✅ Product {i}: {product.name} - ${product.price} ({'created' if created else 'existing'})")

    return category, products


def test_cart_models():
    """Test cart model functionality"""
    print_header("TESTING CART MODELS")

    category, products = create_test_data()

    print_step(1, "Creating cart and adding items")
    cart = Cart.objects.create()
    print(f"   Cart created: {cart}")

    # Add first product
    item1 = CartItem.objects.create(cart=cart, product=products[0], quantity=2)
    print(f"   Added: {item1}")

    # Add second product
    item2 = CartItem.objects.create(cart=cart, product=products[1], quantity=3)
    print(f"   Added: {item2}")

    print_step(2, "Testing cart calculations")
    print(f"   Total items: {cart.total_items}")
    print(f"   Total price: ${cart.total_price}")
    print(f"   Is empty: {cart.is_empty()}")

    print_step(3, "Testing item calculations")
    print(f"   Item 1 total: ${item1.total_price} (${products[0].price} x {item1.quantity})")
    print(f"   Item 2 total: ${item2.total_price} (${products[1].price} x {item2.quantity})")

    print_step(4, "Testing quantity operations")
    original_qty = item1.quantity
    item1.increase_quantity(1)
    print(f"   Increased quantity: {original_qty} → {item1.quantity}")

    item1.decrease_quantity(2)
    print(f"   Decreased quantity: {item1.quantity + 2} → {item1.quantity}")

    print_step(5, "Cleaning up")
    cart.delete()
    print("   Cart and items deleted")

    return category, products


def test_cart_utils():
    """Test cart utility functions"""
    print_header("TESTING CART UTILITIES")

    category, products = create_test_data()

    print_step(1, "Testing anonymous user cart creation")
    factory = RequestFactory()
    request = factory.get('/')

    # Create session
    session = SessionStore()
    session.create()
    request.session = session

    # Mock anonymous user
    from django.contrib.auth.models import AnonymousUser
    request.user = AnonymousUser()

    cart = get_or_create_cart(request)
    print(f"   Anonymous cart created: {cart}")
    print(f"   Session key: {cart.session_key}")

    print_step(2, "Testing authenticated user cart creation")
    user, created = User.objects.get_or_create(username='debuguser')
    request.user = user

    user_cart = get_or_create_cart(request)
    print(f"   User cart created: {user_cart}")
    print(f"   User: {user_cart.user}")

    print_step(3, "Cleaning up")
    if cart:
        cart.delete()
    if user_cart:
        user_cart.delete()
    user.delete()

    return category, products


def test_cart_views():
    """Test cart views using Django test client"""
    print_header("TESTING CART VIEWS")

    category, products = create_test_data()
    client = Client()

    print_step(1, "Testing cart detail view")
    response = client.get(reverse('cart:cart_detail'))
    print(f"   Status code: {response.status_code}")
    print(f"   Template used: {response.templates[0].name if response.templates else 'N/A'}")

    print_step(2, "Testing add to cart")
    add_url = reverse('cart:add_to_cart', args=[products[0].id])
    response = client.post(add_url, {
        'quantity': 2,
        'csrfmiddlewaretoken': client.session.get('csrftoken', 'test')
    }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    print(f"   Status code: {response.status_code}")
    if response.status_code == 200:
        try:
            data = json.loads(response.content)
            print(f"   Response: {data}")
        except json.JSONDecodeError:
            print(f"   Non-JSON response: {response.content[:100]}...")

    print_step(3, "Testing cart count")
    count_response = client.get(reverse('cart:cart_count'))
    print(f"   Status code: {count_response.status_code}")
    if count_response.status_code == 200:
        try:
            count_data = json.loads(count_response.content)
            print(f"   Cart count: {count_data}")
        except json.JSONDecodeError:
            print(f"   Non-JSON response: {count_response.content[:100]}...")

    print_step(4, "Checking database state")
    carts = Cart.objects.all()
    print(f"   Total carts in DB: {carts.count()}")
    for cart in carts:
        print(f"   Cart {cart.id}: {cart.total_items} items, ${cart.total_price}")
        for item in cart.items.all():
            print(f"     - {item.product.name}: {item.quantity}x ${item.product.price}")

    return category, products


def test_template_integration():
    """Test template and URL integration"""
    print_header("TESTING TEMPLATE INTEGRATION")

    category, products = create_test_data()
    client = Client()

    print_step(1, "Testing product detail page")
    detail_url = reverse('products:product_detail', args=[products[0].slug])
    response = client.get(detail_url)
    print(f"   Status code: {response.status_code}")
    print(f"   Contains add to cart form: {'cart:add_to_cart' in response.content.decode()}")

    print_step(2, "Testing product list page")
    list_url = reverse('products:product_list')
    response = client.get(list_url)
    print(f"   Status code: {response.status_code}")
    print(f"   Contains cart buttons: {'Add to Cart' in response.content.decode()}")

    print_step(3, "Testing cart page after adding items")
    # Add an item first
    client.post(reverse('cart:add_to_cart', args=[products[0].id]), {'quantity': 1})

    cart_response = client.get(reverse('cart:cart_detail'))
    print(f"   Status code: {cart_response.status_code}")
    content = cart_response.content.decode()
    print(f"   Contains product name: {products[0].name in content}")
    print(f"   Contains remove button: {'Remove' in content}")

    return category, products


def cleanup_test_data(category, products):
    """Clean up test data"""
    print_header("CLEANING UP TEST DATA")

    # Delete all carts
    carts_deleted = Cart.objects.all().delete()
    print(f"✅ Deleted carts: {carts_deleted}")

    # Delete products
    for product in products:
        product.delete()
        print(f"✅ Deleted product: {product.name}")

    # Delete category
    category.delete()
    print(f"✅ Deleted category: {category.name}")


def main():
    """Run all tests"""
    print("🚀 Starting Cart Functionality Debug Session")
    print(f"Django version: {django.get_version()}")
    print(f"Debug mode: {settings.DEBUG}")

    try:
        # Run tests
        category, products = test_cart_models()
        test_cart_utils()
        test_cart_views()
        test_template_integration()

        print_header("DEBUG SESSION COMPLETED")
        print("✅ All tests completed successfully!")
        print("\nIf you're still experiencing issues:")
        print("1. Check browser console for JavaScript errors")
        print("2. Verify HTMX is loading properly")
        print("3. Check Django server logs for errors")
        print("4. Ensure static files are collected and served")

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Always cleanup
        try:
            cleanup_test_data(category, products)
        except Exception as e:
            print(f"⚠️ Cleanup error: {e}")


if __name__ == '__main__':
    main()
