from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from products.models import Product
from .models import Cart, CartItem
from .utils import get_or_create_cart
import random

def get_quantity_update_message(old_quantity, new_quantity, product_name):
    """Get a user-friendly message for quantity changes"""
    if new_quantity > old_quantity:
        # Quantity increased
        added = new_quantity - old_quantity
        if added == 1:
            return f"Added 1 more {product_name}"
        else:
            return f"Added {added} more {product_name}"
    else:
        # Quantity decreased
        removed = old_quantity - new_quantity
        if removed == 1:
            return f"Removed 1 {product_name}"
        else:
            return f"Removed {removed} {product_name}"

def get_add_message(quantity, product_name):
    """Get a user-friendly message for adding items"""
    if quantity == 1:
        return f"Added {product_name} to cart"
    else:
        return f"Added {quantity} {product_name} to cart"

def get_remove_message(product_name):
    """Get a user-friendly message for removing items"""
    return f"Removed {product_name} from cart"

def get_clear_message():
    """Get a user-friendly message for clearing cart"""
    return "Cart cleared"

def get_empty_message():
    """Get a user-friendly message for already empty cart"""
    return "Cart is already empty"


def cart_detail(request):
    """Display cart contents."""
    cart = get_or_create_cart(request)

    context = {
        'cart': cart,
        'cart_items': cart.items.select_related('product').all() if cart else [],
    }

    return render(request, 'cart/cart_detail.html', context)


@require_POST
def add_to_cart(request, product_id):
    """Add a product to the cart."""
    product = get_object_or_404(Product, id=product_id, is_published=True)
    cart = get_or_create_cart(request)

    # Get quantity from POST data, default to 1
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1

    # Check if item already exists in cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        # Item already exists, update quantity
        old_quantity = cart_item.quantity
        cart_item.quantity += quantity
        cart_item.save()
        # Use specific message for quantity changes
        message = get_quantity_update_message(old_quantity, cart_item.quantity, product.name)
    else:
        # New item added
        message = get_add_message(quantity, product.name)

    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('HX-Request'):
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_count': cart.total_items,
            'cart_total': float(cart.total_price)
        })

    # Handle regular form submissions
    messages.success(request, message)

    # Redirect back to the referring page or product detail
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)

    return redirect('products:product_detail', slug=product.slug)


@require_POST
def update_cart_item(request, item_id):
    """Update quantity of a cart item."""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            # Remove item if quantity is 0 or negative
            product_name = cart_item.product.name
            cart_item.delete()
            message = get_remove_message(product_name)
        else:
            old_quantity = cart_item.quantity
            cart_item.quantity = quantity
            cart_item.save()
            # Use specific message for quantity changes
            message = get_quantity_update_message(old_quantity, quantity, cart_item.product.name)
    except (ValueError, TypeError):
        message = "Please enter a valid number"

    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('HX-Request'):
        if quantity < 1:
            # Item was removed
            return JsonResponse({
                'success': True,
                'message': message,
                'cart_count': cart.total_items,
                'cart_total': float(cart.total_price),
                'item_removed': True
            })
        else:
            return JsonResponse({
                'success': True,
                'message': message,
                'cart_count': cart.total_items,
                'cart_total': float(cart.total_price),
                'item_total': float(cart_item.total_price)
            })

    messages.success(request, message)
    return redirect('cart:cart_detail')


@require_POST
def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()

    message = get_remove_message(product_name)

    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('HX-Request'):
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_count': cart.total_items,
            'cart_total': float(cart.total_price)
        })

    messages.success(request, message)
    return redirect('cart:cart_detail')


@require_POST
def clear_cart(request):
    """Clear all items from the cart."""
    cart = get_or_create_cart(request)

    if cart and not cart.is_empty():
        cart.clear()
        message = get_clear_message()
    else:
        message = get_empty_message()

    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('HX-Request'):
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_count': 0,
            'cart_total': 0.0
        })

    messages.success(request, message)
    return redirect('cart:cart_detail')


def cart_count(request):
    """Return cart count for AJAX requests."""
    cart = get_or_create_cart(request)

    return JsonResponse({
        'cart_count': cart.total_items if cart else 0,
        'cart_total': float(cart.total_price) if cart else 0.0
    })


# HTMX specific views for partial updates
def cart_items_partial(request):
    """Return partial template for cart items (for HTMX updates)."""
    cart = get_or_create_cart(request)

    context = {
        'cart': cart,
        'cart_items': cart.items.select_related('product').all() if cart else [],
    }

    return render(request, 'cart/partials/cart_items.html', context)


def cart_summary_partial(request):
    """Return partial template for cart summary (for HTMX updates)."""
    cart = get_or_create_cart(request)

    context = {
        'cart': cart,
    }

    return render(request, 'cart/partials/cart_summary.html', context)
