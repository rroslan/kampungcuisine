#!/bin/bash

# Email Setup Script for Kampungcuisine
# This script helps you configure email functionality using Resend

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}📧 Kampungcuisine Email Setup${NC}"
echo -e "${CYAN}=============================${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo -e "${RED}❌ Error: manage.py not found. Please run this script from the project root directory.${NC}"
    exit 1
fi

echo -e "${BLUE}This script will help you configure email functionality for Kampungcuisine.${NC}"
echo -e "${BLUE}We use Resend (resend.com) as our email service provider.${NC}"
echo ""

# Check current RESEND_API_KEY status
if [ -n "$RESEND_API_KEY" ]; then
    echo -e "${GREEN}✅ RESEND_API_KEY is already set in your environment${NC}"
    echo -e "${YELLOW}Current key length: ${#RESEND_API_KEY} characters${NC}"
    echo ""
    echo -e "${YELLOW}Would you like to update it? (y/n)${NC}"
    read -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}Keeping existing API key.${NC}"
        SKIP_KEY_SETUP=true
    fi
else
    echo -e "${YELLOW}⚠️  RESEND_API_KEY is not set in your environment${NC}"
fi

# Get API key if needed
if [ "$SKIP_KEY_SETUP" != "true" ]; then
    echo ""
    echo -e "${BLUE}📝 Setting up Resend API Key${NC}"
    echo -e "${BLUE}=============================${NC}"
    echo ""
    echo -e "${YELLOW}To get your Resend API key:${NC}"
    echo -e "1. Go to https://resend.com"
    echo -e "2. Sign up or log in to your account"
    echo -e "3. Go to Settings > API Keys"
    echo -e "4. Create a new API key with 'Sending access'"
    echo -e "5. Copy the API key (it starts with 're_')"
    echo ""
    echo -e "${YELLOW}Please enter your Resend API key:${NC}"
    read -s RESEND_API_KEY
    echo ""

    # Validate API key format
    if [[ ! $RESEND_API_KEY =~ ^re_ ]]; then
        echo -e "${RED}❌ Warning: API key doesn't start with 're_' - this might not be a valid Resend API key${NC}"
        echo -e "${YELLOW}Do you want to continue anyway? (y/n)${NC}"
        read -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${RED}Setup cancelled.${NC}"
            exit 1
        fi
    fi

    if [ -z "$RESEND_API_KEY" ]; then
        echo -e "${RED}❌ No API key provided. Setup cancelled.${NC}"
        exit 1
    fi
fi

# Add to .env file
echo ""
echo -e "${BLUE}📄 Updating environment configuration${NC}"
echo -e "${BLUE}=====================================${NC}"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    touch .env
fi

# Check if RESEND_API_KEY already exists in .env
if grep -q "RESEND_API_KEY" .env; then
    echo -e "${YELLOW}Updating existing RESEND_API_KEY in .env file...${NC}"
    # Use sed to replace the line
    sed -i "s/^RESEND_API_KEY=.*/RESEND_API_KEY=$RESEND_API_KEY/" .env
else
    echo -e "${YELLOW}Adding RESEND_API_KEY to .env file...${NC}"
    echo "RESEND_API_KEY=$RESEND_API_KEY" >> .env
fi

# Check if USE_REAL_EMAIL exists in .env
if ! grep -q "USE_REAL_EMAIL" .env; then
    echo -e "${YELLOW}Adding USE_REAL_EMAIL setting to .env file...${NC}"
    echo "USE_REAL_EMAIL=false" >> .env
fi

echo -e "${GREEN}✅ Environment file updated${NC}"

# Set up verified sender domain
echo ""
echo -e "${BLUE}🔧 Domain Verification${NC}"
echo -e "${BLUE}=====================${NC}"
echo ""
echo -e "${YELLOW}Important: You need to verify your sender domain in Resend${NC}"
echo -e "1. Go to https://resend.com/domains"
echo -e "2. Add your domain (e.g., applikasi.tech)"
echo -e "3. Follow the DNS verification steps"
echo -e "4. Wait for verification to complete"
echo ""
echo -e "${YELLOW}Current sender email: noreply@applikasi.tech${NC}"
echo -e "${YELLOW}Make sure 'applikasi.tech' is verified in your Resend account${NC}"

# Test configuration
echo ""
echo -e "${BLUE}🧪 Testing Email Configuration${NC}"
echo -e "${BLUE}===============================${NC}"
echo ""
echo -e "${YELLOW}Would you like to test the email configuration now? (y/n)${NC}"
read -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Running email test...${NC}"
    echo ""

    # Export the API key for the test
    export RESEND_API_KEY=$RESEND_API_KEY
    export USE_REAL_EMAIL=true

    python test_email.py
fi

# Usage instructions
echo ""
echo -e "${GREEN}🎉 Email Setup Complete!${NC}"
echo -e "${GREEN}========================${NC}"
echo ""
echo -e "${BLUE}How to use email functionality:${NC}"
echo ""
echo -e "${YELLOW}For Development (Console Email):${NC}"
echo -e "   python manage.py runserver --settings=core.settings_dev"
echo -e "   Emails will be printed to the console"
echo ""
echo -e "${YELLOW}For Development (Real Email):${NC}"
echo -e "   export USE_REAL_EMAIL=true"
echo -e "   python manage.py runserver --settings=core.settings_dev"
echo -e "   Emails will be sent via Resend"
echo ""
echo -e "${YELLOW}For Production:${NC}"
echo -e "   Make sure RESEND_API_KEY is set in your production environment"
echo -e "   python manage.py runserver --settings=core.settings_prod"
echo ""
echo -e "${BLUE}Environment Variables:${NC}"
echo -e "   RESEND_API_KEY: Your Resend API key"
echo -e "   USE_REAL_EMAIL: Set to 'true' to enable real emails in development"
echo ""
echo -e "${BLUE}Test Commands:${NC}"
echo -e "   python test_email.py        # Test email configuration"
echo -e "   python manage.py shell      # Test in Django shell"
echo ""
echo -e "${GREEN}Your contact form should now work properly!${NC}"
