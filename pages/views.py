from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from products.models import Product, Category
from .forms import ContactForm

# Create your views here.


def index(request):
    """Render the home page with product listings"""
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

    # Check if this is an HTMX request
    if request.headers.get('HX-Request'):
        # Return only the product grid partial for HTMX requests
        return render(request, 'products/partials/product_grid.html', context)

    # Check if this is a request for category menu
    if request.headers.get('HX-Request') and request.headers.get('HX-Target') in ['category-menu', 'desktop-category-menu']:
        return render(request, 'products/partials/category_menu.html', {'categories': categories})

    return render(request, 'pages/index.html', context)


def about_us(request):
    """Render the about us page"""
    return render(request, 'pages/about.html')


def contact_us(request):
    """Handle contact form display and submission"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Try to send the email
            email_sent = form.send_email()

            if email_sent:
                # Redirect to prevent form resubmission
                return redirect('pages:contact_success')
            else:
                messages.error(
                    request,
                    "Sorry, there was an issue sending your message. Please try again or contact us directly at rroslan@gmail.com."
                )
    else:
        form = ContactForm()

    context = {
        'form': form,
        'page_title': 'Contact Us',
    }
    return render(request, 'pages/contact.html', context)


def contact_success(request):
    """Display contact form success page"""
    return render(request, 'pages/contact_success.html')
