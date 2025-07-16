#!/bin/bash

# Quick Django Template Checker
# This script quickly checks Django templates for formatting and linting issues

echo "🔍 Quick Template Check for Django Templates..."

# Check if djlint is installed
if ! command -v djlint &> /dev/null; then
    echo "❌ djlint is not installed. Please install it with: pip install djlint"
    exit 1
fi

# Function to check templates in a directory
check_directory() {
    local dir=$1
    local name=$2

    if [ -d "$dir" ]; then
        echo "📁 Checking $name..."
        djlint "$dir" --check --quiet
        local exit_code=$?

        if [ $exit_code -eq 0 ]; then
            echo "  ✅ $name templates are properly formatted"
        else
            echo "  ⚠️  $name templates need formatting"
            return 1
        fi
    fi
    return 0
}

# Track if any issues found
issues_found=0

# Check main templates directory
if ! check_directory "templates/" "Main"; then
    issues_found=1
fi

# Check app template directories
for app in accounts cart core orders pages products; do
    if [ -d "$app/templates" ]; then
        if ! check_directory "$app/templates/" "$app"; then
            issues_found=1
        fi
    fi
done

echo ""

# Summary
if [ $issues_found -eq 0 ]; then
    echo "🎉 All templates are properly formatted!"
    echo ""
    echo "💡 To maintain formatting:"
    echo "  - Zed will auto-format on save"
    echo "  - Run './format_templates.sh' to format all templates"
    echo "  - Use djlint tasks in Zed (Cmd+Shift+P → Tasks: Run Task)"
else
    echo "⚠️  Some templates need formatting. Run one of these commands:"
    echo ""
    echo "  ./format_templates.sh           # Format all templates"
    echo "  djlint templates/ --reformat    # Format main templates"
    echo ""
    echo "🔧 In Zed editor:"
    echo "  - Press Cmd+Shift+P (Mac) or Ctrl+Shift+P (Linux)"
    echo "  - Type 'Tasks: Run Task'"
    echo "  - Select 'Format Templates with djlint'"
fi

echo ""
echo "📊 Template Statistics:"
total_templates=$(find templates/ -name "*.html" 2>/dev/null | wc -l)
echo "  Total templates: $total_templates"

# Check for backup files
backup_count=$(find templates/ -name "*.backup" 2>/dev/null | wc -l)
if [ $backup_count -gt 0 ]; then
    echo "  Backup files: $backup_count (consider cleaning up)"
fi

exit $issues_found
