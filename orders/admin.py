from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('total_price',)
    fields = ('product', 'quantity', 'price', 'total_price')

    def total_price(self, obj):
        if obj.id:
            return f"RM {obj.total_price}"
        return "-"
    total_price.short_description = "Total Price"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'status', 'total_amount', 'created_at', 'order_status_badge')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('order_number', 'customer_name', 'customer_email', 'customer_phone')
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'total_items')
    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status')
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_email', 'customer_phone', 'delivery_address')
        }),
        ('Order Details', {
            'fields': ('total_amount', 'total_items', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def order_status_badge(self, obj):
        colors = {
            'pending': '#f39c12',
            'confirmed': '#3498db',
            'preparing': '#e67e22',
            'ready': '#27ae60',
            'delivered': '#2ecc71',
            'cancelled': '#e74c3c',
        }
        color = colors.get(obj.status, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display().upper()
        )
    order_status_badge.short_description = 'Status Badge'
    order_status_badge.admin_order_field = 'status'

    def total_items(self, obj):
        return obj.total_items
    total_items.short_description = 'Total Items'

    actions = ['mark_as_confirmed', 'mark_as_preparing', 'mark_as_ready', 'mark_as_delivered']

    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} orders marked as confirmed.')
    mark_as_confirmed.short_description = 'Mark selected orders as confirmed'

    def mark_as_preparing(self, request, queryset):
        updated = queryset.update(status='preparing')
        self.message_user(request, f'{updated} orders marked as preparing.')
    mark_as_preparing.short_description = 'Mark selected orders as preparing'

    def mark_as_ready(self, request, queryset):
        updated = queryset.update(status='ready')
        self.message_user(request, f'{updated} orders marked as ready.')
    mark_as_ready.short_description = 'Mark selected orders as ready'

    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} orders marked as delivered.')
    mark_as_delivered.short_description = 'Mark selected orders as delivered'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'total_price')
    list_filter = ('order__status', 'order__created_at')
    search_fields = ('order__order_number', 'product__name')
    readonly_fields = ('total_price',)

    def total_price(self, obj):
        return f"RM {obj.total_price}"
    total_price.short_description = "Total Price"
