# Products App

This Django app provides a complete product management system for the Kampung Cuisine e-commerce platform.

## Features

- **Product Management**: Create, read, update, and delete products with multiple images
- **Category System**: Organize products into categories with slugs for SEO-friendly URLs
- **Image Support**: Each product can have up to 4 images (1 main + 3 additional)
- **Publishing Control**: Products can be marked as published/unpublished
- **Admin Interface**: Full-featured Django admin interface with image previews
- **Public Views**: Product listing, category browsing, and product detail pages

## Models

### Category
- `name`: Category name (unique)
- `slug`: URL-friendly version of the name (auto-generated)
- `description`: Optional description text
- Timestamps: `created_at`, `updated_at`

### Product
- `name`: Product name
- `category`: Foreign key to Category (optional)
- `sku`: Stock Keeping Unit (unique)
- `slug`: URL-friendly version of the name (auto-generated)
- `description`: Optional product description
- `price`: Decimal field for product pricing
- `is_published`: Boolean flag for product visibility
- `image_main`: Main product image
- `image_1`, `image_2`, `image_3`: Additional product images
- Timestamps: `created_at`, `updated_at`

## URLs

- `/products/` - Product listing page with search, filtering, and sorting
- `/products/category/<slug>/` - Products filtered by category
- `/products/product/<slug>/` - Individual product detail page

## Admin Features

- **Inline image previews**: See all product images in the admin
- **Bulk actions**: Publish/unpublish multiple products at once
- **List editing**: Edit prices and publishing status directly from the list view
- **Search and filtering**: Find products by name, SKU, or description
- **Category product count**: See how many products are in each category

## Management Commands

### create_sample_products
Creates sample categories and products for testing:

```bash
python manage.py create_sample_products
```

This command will:
- Create 5 sample categories (Cookware, Cutlery, Bakeware, Kitchen Tools, Storage)
- Create 8 sample products with realistic data
- Attach sample images if they exist in the media folder

## Templates

The app includes three main templates:

1. **product_list.html**: Displays all products with:
   - Search functionality
   - Category filtering
   - Sort options (newest, oldest, name A-Z/Z-A, price low-high/high-low)
   - Pagination (12 products per page)
   - Responsive grid layout

2. **category_detail.html**: Shows products in a specific category with:
   - Breadcrumb navigation
   - Product count
   - Pagination
   - Links to other categories

3. **product_detail.html**: Individual product page with:
   - Image gallery with thumbnail navigation
   - Product information (name, price, SKU, description)
   - Category link
   - Related products from the same category
   - Add to cart button (placeholder)

## Media Setup

Product images are stored in:
- Main images: `media/products/main/`
- Additional images: `media/products/additional/`

The media folder structure is created automatically when you run migrations.

## Sample Images

The project includes sample product images that can be downloaded:
- `sample_pot.jpg` - Stock pot image
- `sample_pan.jpg` - Frying pan image
- `sample_knife.jpg` - Kitchen knife image

These are automatically attached to products when running the `create_sample_products` command.

## Development

To set up the products app:

1. Run migrations:
   ```bash
   python manage.py migrate products
   ```

2. Create sample data:
   ```bash
   python manage.py create_sample_products
   ```

3. Access the admin at `/admin/` to manage products

4. View the product catalog at `/products/`

## Styling

The templates use Tailwind CSS with:
- Responsive design that works on all devices
- Hover effects and transitions
- Clean, modern UI components
- DaisyUI components where applicable

## Future Enhancements

Potential improvements that could be added:
- Product variants (size, color, etc.)
- Inventory tracking
- Product reviews and ratings
- Wishlist functionality
- Shopping cart integration
- Product import/export
- Advanced filtering (price range, multiple categories)
- Product recommendations
- SEO metadata fields
