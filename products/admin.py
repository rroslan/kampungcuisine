from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_count', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Number of Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'price', 'is_published', 'image_preview', 'created_at']
    list_filter = ['is_published', 'category', 'created_at', 'updated_at']
    search_fields = ['name', 'sku', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'preview_all_images']
    list_editable = ['is_published', 'price']
    list_per_page = 20

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sku', 'category', 'description')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'is_published')
        }),
        ('Images', {
            'fields': ('image_main', 'image_1', 'image_2', 'image_3', 'preview_all_images'),
            'description': 'Upload product images. Main image will be used as the primary display image.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def image_preview(self, obj):
        if obj.image_main:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.image_main.url
            )
        return "-"
    image_preview.short_description = "Main Image"

    def preview_all_images(self, obj):
        if not obj.pk:
            return "Save the product first to see image previews"

        html = '<div style="display: flex; gap: 10px; flex-wrap: wrap;">'

        if obj.image_main:
            html += format_html(
                '<div><p><strong>Main Image:</strong></p><img src="{}" style="max-height: 200px; max-width: 200px;" /></div>',
                obj.image_main.url
            )

        if obj.image_1:
            html += format_html(
                '<div><p><strong>Image 1:</strong></p><img src="{}" style="max-height: 200px; max-width: 200px;" /></div>',
                obj.image_1.url
            )

        if obj.image_2:
            html += format_html(
                '<div><p><strong>Image 2:</strong></p><img src="{}" style="max-height: 200px; max-width: 200px;" /></div>',
                obj.image_2.url
            )

        if obj.image_3:
            html += format_html(
                '<div><p><strong>Image 3:</strong></p><img src="{}" style="max-height: 200px; max-width: 200px;" /></div>',
                obj.image_3.url
            )

        html += '</div>'

        if not any([obj.image_main, obj.image_1, obj.image_2, obj.image_3]):
            return "No images uploaded"

        return format_html(html)

    preview_all_images.short_description = "All Images Preview"

    actions = ['make_published', 'make_unpublished']

    def make_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f"{updated} product(s) were published.")
    make_published.short_description = "Publish selected products"

    def make_unpublished(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f"{updated} product(s) were unpublished.")
    make_unpublished.short_description = "Unpublish selected products"
