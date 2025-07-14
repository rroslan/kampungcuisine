"""
Context processors for the core application.
These functions add global variables to template contexts.
"""

from products.models import Category
from cart.utils import get_cart_for_request


def categories(request):
    """
    Add all categories to the template context.
    This makes categories available in all templates without explicitly passing them.

    Usage in templates:
    {% for category in categories %}
        <a href="#">{{ category.name }}</a>
    {% endfor %}
    """
    try:
        return {
            'categories': Category.objects.all().order_by('name')
        }
    except Exception:
        # Return empty list if database isn't ready or there's an error
        return {
            'categories': []
        }


def site_info(request):
    """
    Add site-wide information to the template context.
    """
    return {
        'site_name': 'Kampung Cuisine',
        'site_description': 'Authentic Malaysian Cuisine & Spices',
        'site_keywords': 'malaysian food, spices, rendang, curry, sambal',
        'company_name': 'Kampung Cuisine Sdn Bhd',
        'contact_email': 'info@kampungcuisine.com',
        'phone_number': '+60 3-1234 5678',
    }


def cart_info(request):
    """
    Add shopping cart information to the template context.
    """
    cart = get_cart_for_request(request)

    cart_count = 0
    cart_total = 0.00

    if cart:
        cart_count = cart.total_items
        cart_total = float(cart.total_price)

    return {
        'cart_count': cart_count,
        'cart_total': cart_total,
        'cart': cart,
    }


def navigation_context(request):
    """
    Add navigation-related context variables.
    """
    # Get current URL name for active navigation highlighting
    current_url_name = None
    if hasattr(request, 'resolver_match') and request.resolver_match:
        current_url_name = request.resolver_match.url_name

    return {
        'current_url_name': current_url_name,
        'is_homepage': request.path == '/',
        'is_products_page': request.path.startswith('/products/'),
        'is_admin_page': request.path.startswith('/admin/'),
    }
