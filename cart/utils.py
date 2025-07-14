from .models import Cart


def get_or_create_cart(request):
    """
    Get or create a cart for the current user or session.
    Returns the cart instance or None if no cart exists and can't be created.
    """
    cart = None

    if request.user.is_authenticated:
        # For authenticated users, get or create cart by user
        session_key = getattr(request.session, 'session_key', None)
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            defaults={'session_key': session_key}
        )

        # If user was anonymous and now logged in, try to merge session cart
        if created and request.session.session_key:
            try:
                session_cart = Cart.objects.get(
                    session_key=request.session.session_key,
                    user__isnull=True
                )
                # Transfer items from session cart to user cart
                for item in session_cart.items.all():
                    cart_item, item_created = cart.items.get_or_create(
                        product=item.product,
                        defaults={'quantity': item.quantity}
                    )
                    if not item_created:
                        cart_item.quantity += item.quantity
                        cart_item.save()

                # Delete the old session cart
                session_cart.delete()
            except Cart.DoesNotExist:
                pass
    else:
        # For anonymous users, get or create cart by session key
        session_key = getattr(request.session, 'session_key', None)
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        cart, created = Cart.objects.get_or_create(
            session_key=session_key,
            user__isnull=True
        )

    return cart


def get_cart_for_request(request):
    """
    Get existing cart for the current user or session.
    Returns None if no cart exists.
    """
    if request.user.is_authenticated:
        try:
            return Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return None
    else:
        session_key = getattr(request.session, 'session_key', None)
        if session_key:
            try:
                return Cart.objects.get(
                    session_key=session_key,
                    user__isnull=True
                )
            except Cart.DoesNotExist:
                return None
        return None


def merge_session_cart_with_user_cart(request, user_cart):
    """
    Merge session cart items with user cart when user logs in.
    """
    session_key = getattr(request.session, 'session_key', None)
    if not session_key:
        return

    try:
        session_cart = Cart.objects.get(
            session_key=session_key,
            user__isnull=True
        )

        # Transfer items from session cart to user cart
        for session_item in session_cart.items.all():
            user_cart_item, created = user_cart.items.get_or_create(
                product=session_item.product,
                defaults={'quantity': session_item.quantity}
            )

            if not created:
                # Item already exists in user cart, add quantities
                user_cart_item.quantity += session_item.quantity
                user_cart_item.save()

        # Delete the session cart after merging
        session_cart.delete()

    except Cart.DoesNotExist:
        # No session cart to merge
        pass
