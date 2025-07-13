#!/bin/bash

# Kampungcuisine Development Environment Setup Script
# This script sets up the development environment for easier Django commands

echo "🏗️  Setting up Kampungcuisine Development Environment..."

# Set environment variable for Django settings
export DJANGO_SETTINGS_MODULE=core.settings_dev

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📝 Setting Django settings to: ${YELLOW}core.settings_dev${NC}"

# Create .env file for development if it doesn't exist
if [ ! -f .env.dev ]; then
    echo -e "${BLUE}📄 Creating .env.dev file...${NC}"
    cat > .env.dev << EOF
# Development Environment Variables
DJANGO_SETTINGS_MODULE=core.settings_dev
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EOF
    echo -e "${GREEN}✅ Created .env.dev file${NC}"
fi

# Function to run Django commands with proper settings
django_dev() {
    python manage.py "$@" --settings=core.settings_dev
}

# Export the function for use in this shell session
export -f django_dev

echo -e "${GREEN}✅ Development environment configured!${NC}"
echo ""
echo -e "${YELLOW}📋 Available commands:${NC}"
echo -e "  ${BLUE}django_dev migrate${NC}                 - Run migrations"
echo -e "  ${BLUE}django_dev runserver${NC}               - Start development server"
echo -e "  ${BLUE}django_dev shell${NC}                   - Open Django shell"
echo -e "  ${BLUE}django_dev createsuperuser${NC}         - Create admin user"
echo -e "  ${BLUE}django_dev populate_kampungcuisine${NC} - Populate sample data"
echo -e "  ${BLUE}django_dev collectstatic${NC}           - Collect static files"
echo ""
echo -e "${YELLOW}💡 Usage examples:${NC}"
echo -e "  ${BLUE}source dev_setup.sh${NC}               - Load this script"
echo -e "  ${BLUE}django_dev migrate${NC}                 - Instead of 'python manage.py migrate --settings=core.settings_dev'"
echo -e "  ${BLUE}django_dev runserver 8080${NC}          - Run server on port 8080"
echo ""

# Check if database exists and is migrated
if [ -f "db.sqlite3" ]; then
    echo -e "${GREEN}✅ SQLite database found${NC}"

    # Check if tables exist
    TABLES=$(python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_dev')
django.setup()
from django.db import connection
cursor = connection.cursor()
cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table' AND name='products_product';\")
result = cursor.fetchone()
print('exists' if result else 'missing')
" 2>/dev/null)

    if [ "$TABLES" = "exists" ]; then
        echo -e "${GREEN}✅ Database tables exist${NC}"

        # Check if data is populated
        PRODUCTS=$(python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_dev')
django.setup()
from products.models import Product
print(Product.objects.count())
" 2>/dev/null)

        if [ "$PRODUCTS" -gt "0" ]; then
            echo -e "${GREEN}✅ Sample data populated (${PRODUCTS} products)${NC}"
        else
            echo -e "${YELLOW}⚠️  No sample data found${NC}"
            echo -e "  Run: ${BLUE}django_dev populate_kampungcuisine${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Database tables not found${NC}"
        echo -e "  Run: ${BLUE}django_dev migrate${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  SQLite database not found${NC}"
    echo -e "  Run: ${BLUE}django_dev migrate${NC}"
fi

echo ""
echo -e "${BLUE}🚀 Ready to develop! Use the commands above.${NC}"
echo -e "${YELLOW}💡 To make these commands permanent, add 'source $(pwd)/dev_setup.sh' to your ~/.bashrc or ~/.zshrc${NC}"
