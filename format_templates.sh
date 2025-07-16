#!/bin/bash

# Format Django Templates Script
# This script formats all Django HTML templates using djlint

echo "🎨 Formatting Django templates with djlint..."

# Check if djlint is installed
if ! command -v djlint &> /dev/null; then
    echo "❌ djlint is not installed. Please install it with: pip install djlint"
    exit 1
fi

# Format all HTML templates in the templates directory
echo "📁 Formatting templates in templates/ directory..."
djlint templates/ --reformat --quiet

# Check for any linting issues
echo "🔍 Checking for linting issues..."
djlint templates/ --check

# Format any HTML files in app directories
echo "📁 Formatting templates in app directories..."
for app in accounts cart core orders pages products; do
    if [ -d "$app/templates" ]; then
        echo "  Formatting $app/templates/"
        djlint "$app/templates/" --reformat --quiet
        djlint "$app/templates/" --check
    fi
done

# Check for backup files and clean them up if needed
echo "🧹 Checking for backup files..."
backup_files=$(find templates/ -name "*.backup" 2>/dev/null)
if [ -n "$backup_files" ]; then
    echo "  Found backup files:"
    echo "$backup_files"
    echo "  Consider removing them if they're no longer needed"
fi

echo "✅ Template formatting complete!"
echo ""
echo "💡 Tips:"
echo "  - Run 'djlint templates/ --check' to check for issues without formatting"
echo "  - Run 'djlint templates/ --reformat' to format templates"
echo "  - Configure your editor to run djlint on save for automatic formatting"
echo ""
echo "🔧 Zed users: The .zed/settings.json is configured for automatic formatting"
echo "🔧 Use Cmd+Shift+P (Mac) or Ctrl+Shift+P (Linux) and run 'Tasks: Run Task'"
echo "🔧 Select 'Format Templates with djlint' to format all templates"
echo "🔧 Configure your editor to use the .djlintrc file for consistent formatting"
