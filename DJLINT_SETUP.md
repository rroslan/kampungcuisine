# Django Template Formatting with djlint and Zed

This document explains how to use djlint for Django template formatting in your Kampung Cuisine project with the Zed editor.

## What is djlint?

djlint is a tool for linting and formatting Django templates. It helps maintain consistent code style and catches common template issues.

## Setup Complete ✅

Your project is already configured with djlint! Here's what has been set up:

### Configuration Files

1. **`.djlintrc`** - Main configuration file with Django-specific settings
2. **`.zed/settings.json`** - Zed editor configuration for automatic formatting
3. **`.zed/tasks.json`** - Predefined tasks for running djlint commands
4. **`format_templates.sh`** - Script to format all templates at once

## How to Use djlint with Zed

### Automatic Formatting on Save

Your Zed editor is configured to automatically format Django templates when you save them. This happens because of the settings in `.zed/settings.json`.

### Manual Formatting Options

#### Option 1: Using Zed Tasks (Recommended)
1. Open the Command Palette: `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Linux)
2. Type "Tasks: Run Task" and select it
3. Choose from these available tasks:
   - **Format Templates with djlint** - Format all templates
   - **Check Templates with djlint** - Check for issues without formatting
   - **Format Current File with djlint** - Format only the current file
   - **Format All Templates (Script)** - Run the comprehensive formatting script

#### Option 2: Using the Terminal
```bash
# Format all templates
djlint templates/ --reformat

# Check for issues without formatting
djlint templates/ --check

# Format a specific file
djlint templates/base.html --reformat

# Run the comprehensive script
./format_templates.sh
```

## Configuration Details

### .djlintrc Settings Explained

```json
{
    "blank_line_after_tag": "load,extends",     // Add blank lines after these tags
    "blank_line_before_tag": "load,extends",    // Add blank lines before these tags
    "close_void_tags": true,                    // Close self-closing tags properly
    "format_attribute_template_tags": true,     // Format Django template tags in attributes
    "format_css": true,                         // Format CSS within templates
    "format_js": true,                          // Format JavaScript within templates
    "ignore": "H006,H020,H021,H030,H031",      // Ignore specific rules
    "include": "H017,H035,H036",               // Include specific rules
    "indent": 4,                               // Use 4 spaces for indentation
    "max_line_length": 120,                    // Maximum line length
    "max_attribute_length": 70,               // Maximum attribute length before wrapping
    "preserve_blank_lines": true,              // Keep existing blank lines
    "preserve_leading_space": false,           // Remove leading spaces
    "profile": "django",                       // Use Django-specific rules
    "require_pragma": false,                   // Don't require format pragma
    "extension": "html",                       // File extension to process
    "exclude": ".git,.tox,__pycache__,*.min.js,*.min.css,node_modules,*.backup"
}
```

### Ignored Rules Explanation

- **H006**: Img tag should have height and width attributes
- **H020**: Use https for external links
- **H021**: Use https for external scripts
- **H030**: Consider adding meta description
- **H031**: Consider adding meta keywords

These are ignored because they're either not applicable to all templates or handled differently in this project.

## What djlint Does

### Formatting Improvements
- Proper indentation (4 spaces)
- Consistent attribute formatting
- Proper spacing around Django template tags
- Line length management (120 characters max)
- Consistent closing tag formatting

### Example Before/After

**Before:**
```html
{% load tailwind_cli %} {% load django_htmx %}
<div
    class="navbar bg-base-100 shadow-lg z-[9999] relative"
    x-data="{ cartCount: {{ cart_count|default:0 }} }"
>
```

**After:**
```html
{% load tailwind_cli %}

{% load django_htmx %}

<div class="navbar bg-base-100 shadow-lg z-[9999] relative"
     x-data="{ cartCount: {{ cart_count|default:0 }} }">
```

## Troubleshooting

### Common Issues

1. **djlint not found**: Make sure djlint is installed: `pip install djlint`
2. **Formatting not working in Zed**: Check that `.zed/settings.json` exists and has the correct configuration
3. **Wrong indentation**: Verify that your `.djlintrc` has `"indent": 4`

### Checking djlint Status
```bash
# Check if djlint is installed
djlint --version

# Test configuration
djlint templates/base.html --check
```

## Best Practices

1. **Format before committing**: Always run formatting before committing changes
2. **Use the script**: Run `./format_templates.sh` periodically to format all templates
3. **Check for issues**: Use `djlint templates/ --check` to identify potential problems
4. **Consistent style**: Let djlint handle formatting so you can focus on functionality

## Integration with Git

Consider adding this to your Git pre-commit hooks:

```bash
#!/bin/sh
# Pre-commit hook to format Django templates
djlint templates/ --check --quiet
if [ $? -ne 0 ]; then
    echo "Template formatting issues found. Run 'djlint templates/ --reformat' to fix."
    exit 1
fi
```

## Resources

- [djlint Documentation](https://djlint.com/)
- [djlint Rules Reference](https://djlint.com/docs/linter/)
- [Django Template Best Practices](https://docs.djangoproject.com/en/stable/topics/templates/)

---

**Note**: Your templates will now be automatically formatted when you save them in Zed. If you encounter any issues, check the Zed terminal output for error messages.