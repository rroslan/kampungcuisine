from django.core.management.base import BaseCommand
from products.models import Category, Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate kampungcuisine database with categories and sample products'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate kampungcuisine database...'))

        # Create categories
        categories_data = [
            {
                'name': 'Ready to Eat',
                'description': 'Delicious pre-cooked Malaysian dishes ready to serve'
            },
            {
                'name': 'Spice Paste',
                'description': 'Authentic Malaysian spice pastes for cooking'
            },
            {
                'name': 'Spice Blend',
                'description': 'Traditional Malaysian spice blends and seasonings'
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
            else:
                self.stdout.write(f'Category already exists: {category.name}')

        # Create sample products
        products_data = [
            # Ready to Eat products
            {
                'name': 'Rendang Daging',
                'category': 'Ready to Eat',
                'sku': 'RTE-REN-001',
                'description': 'Traditional Minangkabau slow-cooked beef in rich coconut curry. Tender beef chunks in aromatic spices.',
                'price': Decimal('18.90'),
                'is_published': True
            },
            {
                'name': 'Curry Chicken',
                'category': 'Ready to Eat',
                'sku': 'RTE-CUR-001',
                'description': 'Malaysian-style curry chicken with potatoes in coconut milk and spices.',
                'price': Decimal('15.90'),
                'is_published': True
            },
            {
                'name': 'Beef Curry',
                'category': 'Ready to Eat',
                'sku': 'RTE-CUR-002',
                'description': 'Rich and flavorful beef curry with tender meat in aromatic curry sauce.',
                'price': Decimal('19.90'),
                'is_published': True
            },
            {
                'name': 'Ayam Masak Merah',
                'category': 'Ready to Eat',
                'sku': 'RTE-AMM-001',
                'description': 'Chicken cooked in spicy tomato-based sauce with onions and chili.',
                'price': Decimal('16.90'),
                'is_published': True
            },
            {
                'name': 'Sambal Udang',
                'category': 'Ready to Eat',
                'sku': 'RTE-SAM-001',
                'description': 'Fresh prawns cooked in spicy sambal sauce with tamarind and chili.',
                'price': Decimal('22.90'),
                'is_published': True
            },

            # Spice Paste products
            {
                'name': 'Rendang Paste',
                'category': 'Spice Paste',
                'sku': 'SPA-REN-001',
                'description': 'Authentic rendang spice paste made with galangal, lemongrass, chili, and traditional spices.',
                'price': Decimal('8.90'),
                'is_published': True
            },
            {
                'name': 'Curry Paste',
                'category': 'Spice Paste',
                'sku': 'SPA-CUR-001',
                'description': 'Traditional Malaysian curry paste with coconut, chili, and aromatic spices.',
                'price': Decimal('7.90'),
                'is_published': True
            },
            {
                'name': 'Sambal Paste',
                'category': 'Spice Paste',
                'sku': 'SPA-SAM-001',
                'description': 'Fiery sambal paste made with fresh chilies, shallots, and belacan.',
                'price': Decimal('6.90'),
                'is_published': True
            },
            {
                'name': 'Laksa Paste',
                'category': 'Spice Paste',
                'sku': 'SPA-LAK-001',
                'description': 'Aromatic laksa spice paste for authentic Malaysian laksa noodle soup.',
                'price': Decimal('9.90'),
                'is_published': True
            },
            {
                'name': 'Tom Yam Paste',
                'category': 'Spice Paste',
                'sku': 'SPA-TOM-001',
                'description': 'Spicy and sour tom yam paste with lemongrass, galangal, and lime leaves.',
                'price': Decimal('8.50'),
                'is_published': True
            },

            # Spice Blend products
            {
                'name': 'Rendang Spice Blend',
                'category': 'Spice Blend',
                'sku': 'SPB-REN-001',
                'description': 'Dry spice blend for rendang with coriander, cumin, fennel, and other traditional spices.',
                'price': Decimal('5.90'),
                'is_published': True
            },
            {
                'name': 'Curry Powder',
                'category': 'Spice Blend',
                'sku': 'SPB-CUR-001',
                'description': 'Malaysian curry powder blend with turmeric, coriander, cumin, and chili.',
                'price': Decimal('4.90'),
                'is_published': True
            },
            {
                'name': 'Fish Curry Powder',
                'category': 'Spice Blend',
                'sku': 'SPB-FIS-001',
                'description': 'Special spice blend for fish curry with fennel, coriander, and aromatic spices.',
                'price': Decimal('5.50'),
                'is_published': True
            },
            {
                'name': 'Meat Curry Powder',
                'category': 'Spice Blend',
                'sku': 'SPB-MEA-001',
                'description': 'Robust spice blend for meat curry with star anise, cardamom, and traditional spices.',
                'price': Decimal('6.50'),
                'is_published': True
            },
            {
                'name': 'Garam Masala',
                'category': 'Spice Blend',
                'sku': 'SPB-GAR-001',
                'description': 'Traditional garam masala blend with cinnamon, cardamom, cloves, and black pepper.',
                'price': Decimal('7.90'),
                'is_published': True
            },
            {
                'name': 'Biryani Spice Mix',
                'category': 'Spice Blend',
                'sku': 'SPB-BIR-001',
                'description': 'Aromatic spice mix for biryani with saffron, bay leaves, and exotic spices.',
                'price': Decimal('9.50'),
                'is_published': True
            }
        ]

        for product_data in products_data:
            category_name = product_data.pop('category')
            category = categories[category_name]

            product, created = Product.objects.get_or_create(
                sku=product_data['sku'],
                defaults={
                    'category': category,
                    **product_data
                }
            )

            if created:
                self.stdout.write(f'Created product: {product.name} ({product.sku})')
            else:
                self.stdout.write(f'Product already exists: {product.name} ({product.sku})')

        # Summary
        total_categories = Category.objects.count()
        total_products = Product.objects.count()

        self.stdout.write(self.style.SUCCESS(f'\nDatabase population completed!'))
        self.stdout.write(self.style.SUCCESS(f'Total categories: {total_categories}'))
        self.stdout.write(self.style.SUCCESS(f'Total products: {total_products}'))

        # Display categories with product counts
        self.stdout.write(self.style.SUCCESS('\nCategories summary:'))
        for category in Category.objects.all():
            product_count = category.products.count()
            self.stdout.write(f'- {category.name}: {product_count} products')
