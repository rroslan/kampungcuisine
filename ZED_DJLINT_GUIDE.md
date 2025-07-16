# Zed Editor + djlint Integration Guide

This guide shows you how to use djlint for Django template formatting with the Zed editor in your Kampung Cuisine project.

## 🎯 Overview

Your project is configured to automatically format Django templates using djlint when you save files in Zed. This ensures consistent code style and catches common template issues.

## 📁 Configuration Files

### 1. `.zed/settings.json` - Main Zed Configuration

```json
{
    "languages": {
        "HTML": {
            "formatter": {
                "external": {
                    "command": "djlint",
                    "arguments": ["--reformat", "--quiet", "${file}"]
                }
            },
            "format_on_save": "on",
            "tab_size": 4,
            "hard_tabs": false
        }
    },
    "format_on_save": "on",
    "tab_size": 4,
    "hard_tabs": false,
    "preferred_line_length": 120
}
```

### 2. `.djlintrc` - djlint Configuration

```json
{
    "profile": "django",
    "indent": 4,
    "max_line_length": 120,
    "format_on_save": true,
    "ignore": "H006,H020,H021,H030,H031"
}
```

## 🚀 How It Works

### Automatic Formatting (Recommended)

1. **Open any Django template** (`.html` file) in Zed
2. **Make changes** to the template
3. **Save the file** (`Cmd+S` or `Ctrl+S`)
4. **djlint automatically formats** the template

### Manual Formatting Options

#### Option 1: Using Zed Tasks

1. Open Command Palette: `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Linux)
2. Type "task: spawn" or "Tasks: Run Task"
3. Select from available tasks:
    - **Format Templates with djlint** - Format all templates in templates/ directory
    - **Check Templates with djlint** - Check all templates for issues
    - **Format Current File with djlint** - Format only the currently open file
    - **Check Current File with djlint** - Check only the currently open file
    - **Format All Templates (Script)** - Run comprehensive formatting script
    - **Check Template Health** - Run health check script

#### Option 2: Using Terminal

```bash
# Format all templates
djlint templates/ --reformat

# Format specific file
djlint templates/base.html --reformat --quiet

# Check for issues without formatting
djlint templates/ --check

# Use project scripts
./format_templates.sh
./check_templates.sh
```

## 🎨 What djlint Does

### Before Formatting:

```html
{% load tailwind_cli %} {% load static %}
<div class="container mx-auto" x-data="{ open: false }">
    <h1>{{ title }}</h1>
</div>
```

### After Formatting:

```html
{% load tailwind_cli %} {% load static %}

<div class="container mx-auto" x-data="{ open: false }">
    <h1>{{ title }}</h1>
</div>
```

### Key Improvements:

- ✅ Proper indentation (4 spaces)
- ✅ Separated `{% load %}` tags with blank lines
- ✅ Consistent attribute formatting
- ✅ Line length management (120 characters)
- ✅ Proper Django template tag spacing

## ⚙️ Customizing Your Setup

### Modify Formatter Behavior

Edit `.zed/settings.json` to change formatter arguments:

```json
{
    "languages": {
        "HTML": {
            "formatter": {
                "external": {
                    "command": "djlint",
                    "arguments": [
                        "--reformat",
                        "--quiet",
                        "--check", // Add this to check before formatting
                        "${file}"
                    ]
                }
            }
        }
    }
}
```

### Change djlint Rules

Edit `.djlintrc` to modify formatting rules:

```json
{
    "profile": "django",
    "indent": 2, // Change to 2 spaces
    "max_line_length": 100, // Shorter lines
    "ignore": "H006,H020", // Ignore fewer rules
    "include": "H017,H035" // Include specific rules
}
```

## 🔧 Troubleshooting

### Issue: Formatting Not Working

**Check:**

1. djlint is installed: `pip list | grep djlint`
2. `.zed/settings.json` exists and is valid JSON
3. File has `.html` extension

**Fix:**

```bash
# Reinstall djlint
pip install djlint

# Test manually
djlint templates/base.html --check
```

### Issue: Wrong Formatting Style

**Check:** `.djlintrc` configuration matches your preferences

**Fix:** Adjust settings in `.djlintrc`:

```json
{
    "indent": 4, // Your preferred indentation
    "max_line_length": 120, // Your preferred line length
    "profile": "django" // Keep this for Django projects
}
```

### Issue: Zed Not Using djlint

**Check:**

1. Zed settings are correct
2. File association is set to HTML
3. Format on save is enabled

**Fix:** Restart Zed or manually run:

- `Cmd+Shift+P` → "Editor: Format Document"

## 📝 File Associations

Make sure your Django templates are recognized as HTML:

### In `.zed/settings.json`:

All `.html` files are automatically treated as HTML files and will use the djlint formatter.

## 📋 Available Tasks

Your project includes predefined tasks that you can run via the Command Palette:

### `.zed/tasks.json` Configuration:

```json
[
    {
        "label": "Format Templates with djlint",
        "command": "djlint",
        "args": ["templates/", "--reformat"],
        "use_new_terminal": false,
        "reveal": "always"
    },
    {
        "label": "Check Templates with djlint",
        "command": "djlint",
        "args": ["templates/", "--check"],
        "use_new_terminal": false,
        "reveal": "always"
    },
    {
        "label": "Format Current File with djlint",
        "command": "djlint",
        "args": ["${file}", "--reformat", "--quiet"],
        "use_new_terminal": false,
        "reveal": "no_focus"
    }
]
```

### How to Use Tasks:

1. **Open Command Palette**: `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Linux)
2. **Type**: "task: spawn"
3. **Select** your desired task from the list
4. **Rerun** the last task with `task: rerun` (default: `Option-T` on Mac)

### Manual Override in Zed:

1. Open a template file
2. Click the language indicator in the status bar
3. Select "HTML" to ensure djlint formatting is applied

## 🎯 Best Practices

### 1. Use Consistent Formatting

- Let djlint handle all formatting automatically
- Don't manually adjust djlint-formatted code
- Focus on functionality, not formatting

### 2. Regular Maintenance

```bash
# Weekly template check
./check_templates.sh

# Format all templates if needed
./format_templates.sh
```

### 3. Team Collaboration

- Commit `.zed/` and `.djlintrc` files to git
- Ensure all team members use the same configuration
- Run formatting before committing changes

## 📊 Project Status

Current template statistics:

- **Total templates**: 20
- **All templates formatted**: ✅
- **Configuration complete**: ✅
- **Auto-format on save**: ✅

## 🔗 Quick Reference

### Essential Commands

```bash
# Check all templates
djlint templates/ --check

# Format all templates
djlint templates/ --reformat

# Format specific file quietly
djlint path/to/file.html --reformat --quiet

# Use project scripts
./format_templates.sh     # Complete formatting
./check_templates.sh      # Quick status check
```

### Zed Shortcuts

- `Cmd+S` / `Ctrl+S` - Save and auto-format
- `Cmd+Shift+P` / `Ctrl+Shift+P` - Command palette
- `Cmd+K, Cmd+F` / `Ctrl+K, Ctrl+F` - Format document manually
- `Option-T` / `Alt-T` - Rerun last task
- Type "task: spawn" in Command Palette - Show all available tasks

## 📚 Additional Resources

- [djlint Documentation](https://djlint.com/)
- [Zed Editor Documentation](https://zed.dev/docs)
- [Django Template Best Practices](https://docs.djangoproject.com/en/stable/topics/templates/)

---

**Your Django templates will now be automatically formatted when saved in Zed!** 🎉

If you encounter any issues, check the Zed terminal output for error messages or run the troubleshooting commands above.
