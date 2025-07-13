#!/bin/bash

# Kampungcuisine Development Server Startup Script
# This script starts the Django development server with the correct settings

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Kampungcuisine Development Server...${NC}"

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo -e "${RED}❌ Error: manage.py not found. Please run this script from the project root directory.${NC}"
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not detected. Activating venv...${NC}"
    if [ -d "venv" ]; then
        source venv/bin/activate
        echo -e "${GREEN}✅ Virtual environment activated${NC}"
    else
        echo -e "${RED}❌ Virtual environment not found. Please create one with: python -m venv venv${NC}"
        exit 1
    fi
fi

# Set default port
PORT=${1:-8000}

# Set default host
HOST=${2:-127.0.0.1}

echo -e "${BLUE}📋 Server Configuration:${NC}"
echo -e "  Host: ${YELLOW}$HOST${NC}"
echo -e "  Port: ${YELLOW}$PORT${NC}"
echo -e "  Settings: ${YELLOW}core.settings_dev${NC}"
echo -e "  Database: ${YELLOW}SQLite (db.sqlite3)${NC}"
echo ""

# Check if database exists and is migrated
if [ ! -f "db.sqlite3" ]; then
    echo -e "${YELLOW}⚠️  Database not found. Running migrations...${NC}"
    python manage.py migrate --settings=core.settings_dev

    # Ask if user wants to populate sample data
    echo -e "${YELLOW}💡 Would you like to populate the database with sample data? (y/n)${NC}"
    read -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}📝 Populating database with sample data...${NC}"
        python manage.py populate_kampungcuisine --settings=core.settings_dev
    fi
fi

# Check if admin user exists
ADMIN_EXISTS=$(python manage.py shell --settings=core.settings_dev -c "from django.contrib.auth.models import User; print('yes' if User.objects.filter(is_superuser=True).exists() else 'no')" 2>/dev/null)

if [ "$ADMIN_EXISTS" = "no" ]; then
    echo -e "${YELLOW}💡 No admin user found. Would you like to create one? (y/n)${NC}"
    read -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python manage.py createsuperuser --settings=core.settings_dev
    fi
fi

echo -e "${GREEN}✅ Starting development server...${NC}"
echo -e "${BLUE}🌐 Server will be available at: http://$HOST:$PORT${NC}"
echo -e "${BLUE}🔧 Admin panel: http://$HOST:$PORT/admin${NC}"
echo -e "${YELLOW}💡 Press Ctrl+C to stop the server${NC}"
echo ""

# Start the server with Tailwind
export DJANGO_SETTINGS_MODULE=core.settings_dev
python manage.py tailwind runserver $HOST:$PORT
