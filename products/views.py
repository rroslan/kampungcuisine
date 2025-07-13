from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category


def product_list(request):
    """Display all published products with filtering and pagination."""
    products = Product.objects.filter(is_published=True).select_related('category')

    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(sku__icontains=query)
        )

    # Category filtering
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Sorting
    sort = request.GET.get('sort', '-created_at')
    if sort in ['name', '-name', 'price', '-price', 'created_at', '-created_at']:
        products = products.order_by(sort)

    # Pagination
    paginator = Paginator(products, 4)  # Show 4 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get all categories for filter sidebar
    categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'products': page_obj,
        'categories': categories,
        'current_category': category_slug,
        'query': query,
        'sort': sort,
    }

    return render(request, 'products/product_list.html', context)


def category_detail(request, slug):
    """Display products in a specific category."""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(
        category=category,
        is_published=True
    ).order_by('-created_at')

    # Pagination
    paginator = Paginator(products, 4)  # Show 4 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
        'products': page_obj,
        'all_categories': Category.objects.all().exclude(id=category.id),
    }

    return render(request, 'products/category_detail.html', context)


def product_detail(request, slug):
    """Display a single product with all its details."""
    product = get_object_or_404(Product, slug=slug, is_published=True)

    # Get related products from the same category
    related_products = Product.objects.filter(
        category=product.category,
        is_published=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }

    # Check if this is an HTMX request for modal content
    if request.headers.get('HX-Request'):
        return render(request, 'products/partials/product_modal.html', context)

    return render(request, 'products/product_detail.html', context)
