from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('added_at', 'updated_at', 'total_price')
    fields = ('product', 'quantity', 'total_price', 'added_at', 'updated_at')

    def total_price(self, obj):
        return f"${obj.total_price:.2f}" if obj.total_price else "$0.00"
    total_price.short_description = 'Total Price'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key_short', 'total_items', 'total_price_display', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'session_key')
    readonly_fields = ('created_at', 'updated_at', 'total_items', 'total_price_display')
    inlines = [CartItemInline]

    def session_key_short(self, obj):
        if obj.session_key:
            return f"{obj.session_key[:8]}..."
        return "N/A"
    session_key_short.short_description = 'Session Key'

    def total_price_display(self, obj):
        return f"${obj.total_price:.2f}"
    total_price_display.short_description = 'Total Price'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'total_price_display', 'added_at', 'updated_at')
    list_filter = ('added_at', 'updated_at', 'product__category')
    search_fields = ('product__name', 'product__sku', 'cart__user__username')
    readonly_fields = ('added_at', 'updated_at', 'total_price_display')

    def total_price_display(self, obj):
        return f"${obj.total_price:.2f}"
    total_price_display.short_description = 'Total Price'
