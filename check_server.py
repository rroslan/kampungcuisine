#!/usr/bin/env python
"""
Kampungcuisine Server Diagnostic Script
Checks if all components are ready for server startup.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_colored(message, color=Colors.WHITE):
    """Print colored message to terminal"""
    print(f"{color}{message}{Colors.END}")

def print_header(title):
    """Print section header"""
    print()
    print_colored("=" * 60, Colors.CYAN)
    print_colored(f"🔍 {title}", Colors.BOLD + Colors.YELLOW)
    print_colored("=" * 60, Colors.CYAN)

def check_item(description, condition, success_msg="OK", error_msg="FAILED"):
    """Check a single item and print result"""
    status = "✅" if condition else "❌"
    color = Colors.GREEN if condition else Colors.RED
    msg = success_msg if condition else error_msg
    print_colored(f"{status} {description}: {msg}", color)
    return condition

def run_django_command(command, settings="core.settings_dev", capture_output=True):
    """Run Django management command"""
    full_command = f"python manage.py {command} --settings={settings}"
    try:
        result = subprocess.run(
            full_command,
            shell=True,
            capture_output=capture_output,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def check_environment():
    """Check Python environment"""
    print_header("ENVIRONMENT CHECK")

    # Python version
    python_version = sys.version_info
    python_ok = python_version.major == 3 and python_version.minor >= 8
    check_item(
        "Python Version",
        python_ok,
        f"{python_version.major}.{python_version.minor}.{python_version.micro}",
        f"{python_version.major}.{python_version.minor}.{python_version.micro} (need 3.8+)"
    )

    # Virtual environment
    venv_active = bool(os.environ.get('VIRTUAL_ENV'))
    check_item(
        "Virtual Environment",
        venv_active,
        os.environ.get('VIRTUAL_ENV', ''),
        "Not activated"
    )

    # Working directory
    cwd = Path.cwd()
    manage_py_exists = (cwd / 'manage.py').exists()
    check_item(
        "Working Directory",
        manage_py_exists,
        str(cwd),
        "manage.py not found in current directory"
    )

    return python_ok and venv_active and manage_py_exists

def check_django_setup():
    """Check Django configuration"""
    print_header("DJANGO CONFIGURATION")

    # Django check command
    success, stdout, stderr = run_django_command("check")
    check_item(
        "Django System Check",
        success,
        "No issues found",
        f"Issues found: {stderr}"
    )

    # Settings files
    settings_files = [
        'core/settings.py',
        'core/settings_dev.py',
        'core/settings_prod.py',
        'core/settings_test.py'
    ]

    for settings_file in settings_files:
        exists = Path(settings_file).exists()
        check_item(f"Settings File ({settings_file})", exists)

    # Context processors
    context_processor_file = Path('core/context_processors.py')
    check_item(
        "Context Processors",
        context_processor_file.exists(),
        "core/context_processors.py found",
        "core/context_processors.py missing"
    )

    return success

def check_database():
    """Check database status"""
    print_header("DATABASE STATUS")

    # Database file (SQLite)
    db_file = Path('db.sqlite3')
    db_exists = db_file.exists()
    check_item(
        "SQLite Database File",
        db_exists,
        f"Found ({db_file.stat().st_size} bytes)" if db_exists else "",
        "Database file not found"
    )

    # Migration status
    success, stdout, stderr = run_django_command("showmigrations --plan")
    migrations_ok = success and "[ ]" not in stdout
    check_item(
        "Database Migrations",
        migrations_ok,
        "All migrations applied",
        "Pending migrations found" if success else "Migration check failed"
    )

    # Check if we can connect to database
    success, stdout, stderr = run_django_command(
        'shell -c "from django.db import connection; connection.cursor(); print(\'OK\')"'
    )
    check_item(
        "Database Connection",
        success,
        "Connection successful",
        f"Connection failed: {stderr}"
    )

    return db_exists and migrations_ok and success

def check_data():
    """Check if sample data is populated"""
    print_header("DATA STATUS")

    # Check categories
    success, stdout, stderr = run_django_command(
        'shell -c "from products.models import Category; print(Category.objects.count())"'
    )
    if success:
        try:
            category_count = int(stdout.strip())
            check_item(
                "Categories",
                category_count > 0,
                f"{category_count} categories found",
                "No categories found"
            )
        except ValueError:
            category_count = 0
            check_item("Categories", False, "", "Could not count categories")
    else:
        category_count = 0
        check_item("Categories", False, "", f"Error: {stderr}")

    # Check products
    success, stdout, stderr = run_django_command(
        'shell -c "from products.models import Product; print(Product.objects.count())"'
    )
    if success:
        try:
            product_count = int(stdout.strip())
            check_item(
                "Products",
                product_count > 0,
                f"{product_count} products found",
                "No products found"
            )
        except ValueError:
            product_count = 0
            check_item("Products", False, "", "Could not count products")
    else:
        product_count = 0
        check_item("Products", False, "", f"Error: {stderr}")

    # Check admin user
    success, stdout, stderr = run_django_command(
        'shell -c "from django.contrib.auth.models import User; print(\'yes\' if User.objects.filter(is_superuser=True).exists() else \'no\')"'
    )
    if success:
        has_admin = 'yes' in stdout.strip().lower()
        check_item(
            "Admin User",
            has_admin,
            "Admin user exists",
            "No admin user found"
        )
    else:
        has_admin = False
        check_item("Admin User", False, "", f"Error: {stderr}")

    return category_count > 0 and product_count > 0

def check_ports():
    """Check if ports are available"""
    print_header("PORT AVAILABILITY")

    try:
        import socket

        def is_port_free(port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('127.0.0.1', port))
                    return True
                except OSError:
                    return False

        common_ports = [8000, 8080, 8001, 8888]

        for port in common_ports:
            is_free = is_port_free(port)
            check_item(
                f"Port {port}",
                is_free,
                "Available",
                "In use"
            )

    except ImportError:
        check_item("Port Check", False, "", "Socket module not available")

def check_static_files():
    """Check static files configuration"""
    print_header("STATIC FILES")

    # Check static directories
    static_dirs = ['assets', 'staticfiles']
    for static_dir in static_dirs:
        dir_path = Path(static_dir)
        exists = dir_path.exists()
        check_item(
            f"Static Directory ({static_dir})",
            exists,
            f"Found ({len(list(dir_path.iterdir())) if exists else 0} items)",
            "Directory not found"
        )

    # Check collectstatic (only check, don't run)
    success, stdout, stderr = run_django_command("collectstatic --dry-run --noinput")
    check_item(
        "Static Files Collection",
        success,
        "Ready to collect",
        f"Collection failed: {stderr}"
    )

def generate_summary():
    """Generate summary and recommendations"""
    print_header("SUMMARY & RECOMMENDATIONS")

    # Run all checks
    env_ok = check_environment()
    django_ok = check_django_setup()
    db_ok = check_database()
    data_ok = check_data()

    print()
    print_colored("📋 QUICK ACTIONS:", Colors.BOLD + Colors.BLUE)

    if not env_ok:
        print_colored("1. Activate virtual environment: source venv/bin/activate", Colors.YELLOW)

    if not django_ok:
        print_colored("2. Fix Django configuration issues", Colors.YELLOW)

    if not db_ok:
        print_colored("3. Run migrations: python manage.py migrate --settings=core.settings_dev", Colors.YELLOW)

    if not data_ok:
        print_colored("4. Populate data: python manage.py populate_kampungcuisine --settings=core.settings_dev", Colors.YELLOW)
        print_colored("5. Create admin: python manage.py createsuperuser --settings=core.settings_dev", Colors.YELLOW)

    print()
    if env_ok and django_ok and db_ok:
        print_colored("🚀 READY TO START SERVER:", Colors.BOLD + Colors.GREEN)
        print_colored("   python manage.py runserver --settings=core.settings_dev", Colors.WHITE)
        print_colored("   ./start_dev.sh", Colors.WHITE)
        print_colored("   python manage_server.py --auto-yes", Colors.WHITE)
    else:
        print_colored("⚠️  RESOLVE ISSUES ABOVE BEFORE STARTING SERVER", Colors.BOLD + Colors.RED)

def main():
    """Main function"""
    print_colored("🍜 KAMPUNGCUISINE SERVER DIAGNOSTIC", Colors.BOLD + Colors.CYAN)
    print_colored("Checking server readiness...", Colors.WHITE)

    try:
        generate_summary()
        check_ports()
        check_static_files()

        print()
        print_colored("💡 TIP: Run this script anytime to check server status!", Colors.BLUE)
        print_colored("Usage: python check_server.py", Colors.WHITE)

    except KeyboardInterrupt:
        print_colored("\n🛑 Check interrupted by user", Colors.YELLOW)
    except Exception as e:
        print_colored(f"\n❌ Unexpected error: {e}", Colors.RED)

if __name__ == '__main__':
    main()
