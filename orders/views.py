from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from cart.utils import get_or_create_cart
from .models import Order, OrderItem
from .forms import CheckoutForm



def checkout_view(request):
    """Checkout process - requires user to be logged in"""
    cart = get_or_create_cart(request)

    if not cart or cart.is_empty():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')

    if not request.user.is_authenticated:
        messages.info(request, 'Please log in to complete your order.')
        return redirect('accounts:login')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create the order
            order = Order.objects.create(
                user=request.user,
                customer_name=form.cleaned_data['customer_name'],
                customer_email=form.cleaned_data['customer_email'],
                customer_phone=form.cleaned_data['customer_phone'],
                delivery_address=form.cleaned_data['delivery_address'],
                notes=form.cleaned_data.get('notes', ''),
                total_amount=cart.total_price
            )

            # Create order items from cart
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            # Clear the cart
            cart.clear()

            # Send confirmation email (optional)
            try:
                send_order_confirmation_email(order)
            except Exception as e:
                print(f"Failed to send confirmation email: {e}")

            messages.success(request, f'Order {order.order_number} placed successfully!')
            return redirect('orders:order_detail', order_number=order.order_number)
    else:
        # Pre-fill form with user data
        initial_data = {
            'customer_name': request.user.get_full_name() or request.user.username,
            'customer_email': request.user.email,
        }

        # Try to get phone from user profile
        if hasattr(request.user, 'userprofile'):
            initial_data['customer_phone'] = request.user.userprofile.phone_number
            initial_data['delivery_address'] = request.user.userprofile.address

        form = CheckoutForm(initial=initial_data)

    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart.items.select_related('product').all(),
    }

    return render(request, 'orders/checkout.html', context)


@login_required
def order_detail_view(request, order_number):
    """View order details"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)

    context = {
        'order': order,
        'order_items': order.items.select_related('product').all(),
    }

    return render(request, 'orders/order_detail.html', context)


@login_required
def order_list_view(request):
    """List user's orders"""
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')

    context = {
        'orders': orders,
    }

    return render(request, 'orders/order_list.html', context)


@login_required
@require_POST
def cancel_order_view(request, order_number):
    """Cancel an order (only if status is pending)"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)

    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, f'Order {order.order_number} has been cancelled.')
    else:
        messages.error(request, 'This order cannot be cancelled.')

    return redirect('orders:order_detail', order_number=order.order_number)


def send_order_confirmation_email(order):
    """Send order confirmation email to customer"""
    subject = f'Order Confirmation - {order.order_number}'

    # Render email template
    html_message = render_to_string('orders/emails/order_confirmation.html', {
        'order': order,
        'order_items': order.items.select_related('product').all(),
    })

    # Send email
    send_mail(
        subject=subject,
        message='',  # Plain text version (optional)
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.customer_email],
        fail_silently=False,
    )
