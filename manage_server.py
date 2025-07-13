#!/usr/bin/env python
"""
Kampungcuisine Server Management Script
A comprehensive tool to manage Django development, testing, and production servers.
"""

import os
import sys
import subprocess
import argparse
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
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_colored(message, color=Colors.WHITE):
    """Print colored message to terminal"""
    print(f"{color}{message}{Colors.END}")

def print_banner():
    """Print welcome banner"""
    print_colored("=" * 60, Colors.CYAN)
    print_colored("🍜 KAMPUNGCUISINE SERVER MANAGER 🍜", Colors.BOLD + Colors.YELLOW)
    print_colored("=" * 60, Colors.CYAN)
    print()

def check_virtual_env():
    """Check if virtual environment is activated"""
    if not os.environ.get('VIRTUAL_ENV'):
        print_colored("⚠️  Warning: Virtual environment not detected", Colors.YELLOW)
        venv_path = Path('venv')
        if venv_path.exists():
            print_colored("💡 Found venv directory. Please activate it:", Colors.BLUE)
            print_colored("   source venv/bin/activate  # Linux/Mac", Colors.WHITE)
            print_colored("   venv\\Scripts\\activate     # Windows", Colors.WHITE)
            return False
        else:
            print_colored("❌ Virtual environment not found", Colors.RED)
            print_colored("💡 Create one with: python -m venv venv", Colors.BLUE)
            return False
    else:
        print_colored(f"✅ Virtual environment active: {os.environ.get('VIRTUAL_ENV')}", Colors.GREEN)
        return True

def run_command(command, settings_module, check_only=False):
    """Run Django management command with specified settings"""
    full_command = f"python manage.py {command} --settings={settings_module}"

    if check_only:
        print_colored(f"Would run: {full_command}", Colors.BLUE)
        return True

    print_colored(f"Running: {full_command}", Colors.BLUE)
    try:
        result = subprocess.run(full_command, shell=True, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ Command failed with exit code {e.returncode}", Colors.RED)
        return False

def check_database(settings_module):
    """Check database status"""
    print_colored("🔍 Checking database status...", Colors.BLUE)

    # Check if migrations are needed
    check_cmd = f"python manage.py showmigrations --settings={settings_module}"
    try:
        result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print_colored("✅ Database connection successful", Colors.GREEN)
            return True
        else:
            print_colored("❌ Database connection failed", Colors.RED)
            print_colored(result.stderr, Colors.RED)
            return False
    except Exception as e:
        print_colored(f"❌ Database check failed: {e}", Colors.RED)
        return False

def migrate_database(settings_module):
    """Run database migrations"""
    print_colored("🔄 Running database migrations...", Colors.BLUE)
    return run_command("migrate", settings_module)

def populate_sample_data(settings_module):
    """Populate database with sample data"""
    print_colored("📝 Populating sample data...", Colors.BLUE)
    return run_command("populate_kampungcuisine", settings_module)

def create_superuser(settings_module):
    """Create Django superuser"""
    print_colored("👤 Creating superuser...", Colors.BLUE)
    return run_command("createsuperuser", settings_module)

def collect_static(settings_module):
    """Collect static files"""
    print_colored("📂 Collecting static files...", Colors.BLUE)
    return run_command("collectstatic --noinput", settings_module)

def start_server(host, port, settings_module):
    """Start Django development server"""
    print_colored(f"🚀 Starting server on {host}:{port}...", Colors.GREEN)
    print_colored(f"📊 Settings: {settings_module}", Colors.BLUE)
    print_colored(f"🌐 Server URL: http://{host}:{port}", Colors.CYAN)
    print_colored(f"🔧 Admin URL: http://{host}:{port}/admin", Colors.CYAN)
    print()
    print_colored("Press Ctrl+C to stop the server", Colors.YELLOW)
    print_colored("-" * 50, Colors.CYAN)

    server_cmd = f"python manage.py runserver {host}:{port} --settings={settings_module}"
    try:
        subprocess.run(server_cmd, shell=True, check=True)
    except KeyboardInterrupt:
        print_colored("\n🛑 Server stopped by user", Colors.YELLOW)
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ Server failed to start: {e}", Colors.RED)

def setup_environment(settings_module, auto_yes=False):
    """Setup development environment"""
    print_colored("🏗️  Setting up environment...", Colors.BLUE)

    # Check database
    if not check_database(settings_module):
        if auto_yes or input("Run migrations? (y/n): ").lower() == 'y':
            if not migrate_database(settings_module):
                return False

    # Check if sample data exists (only for dev/test environments)
    if 'dev' in settings_module or 'test' in settings_module:
        try:
            check_cmd = f"python manage.py shell --settings={settings_module} -c \"from products.models import Product; print(Product.objects.count())\""
            result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0 and int(result.stdout.strip()) == 0:
                if auto_yes or input("Populate sample data? (y/n): ").lower() == 'y':
                    populate_sample_data(settings_module)
        except:
            pass

    # Check for superuser (optional)
    try:
        check_cmd = f"python manage.py shell --settings={settings_module} -c \"from django.contrib.auth.models import User; print('yes' if User.objects.filter(is_superuser=True).exists() else 'no')\""
        result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0 and 'no' in result.stdout:
            if auto_yes or input("Create superuser? (y/n): ").lower() == 'y':
                create_superuser(settings_module)
    except:
        pass

    print_colored("✅ Environment setup complete!", Colors.GREEN)
    return True

def main():
    """Main function"""
    print_banner()

    parser = argparse.ArgumentParser(description='Kampungcuisine Server Manager')
    parser.add_argument('--env', choices=['dev', 'prod', 'test'], default='dev',
                       help='Environment to use (default: dev)')
    parser.add_argument('--host', default='127.0.0.1',
                       help='Host to bind server to (default: 127.0.0.1)')
    parser.add_argument('--port', default='8000',
                       help='Port to run server on (default: 8000)')
    parser.add_argument('--no-setup', action='store_true',
                       help='Skip environment setup')
    parser.add_argument('--setup-only', action='store_true',
                       help='Only run setup, don\'t start server')
    parser.add_argument('--auto-yes', action='store_true',
                       help='Automatically answer yes to all prompts')
    parser.add_argument('--collect-static', action='store_true',
                       help='Collect static files before starting')

    args = parser.parse_args()

    # Map environment to settings module
    settings_map = {
        'dev': 'core.settings_dev',
        'prod': 'core.settings_prod',
        'test': 'core.settings_test'
    }

    settings_module = settings_map[args.env]

    print_colored(f"🔧 Environment: {args.env.upper()}", Colors.PURPLE)
    print_colored(f"⚙️  Settings: {settings_module}", Colors.BLUE)
    print()

    # Check virtual environment
    if not check_virtual_env():
        sys.exit(1)

    # Setup environment if not skipped
    if not args.no_setup:
        if not setup_environment(settings_module, args.auto_yes):
            print_colored("❌ Environment setup failed", Colors.RED)
            sys.exit(1)

    # Collect static files if requested
    if args.collect_static:
        collect_static(settings_module)

    # Exit if setup-only
    if args.setup_only:
        print_colored("✅ Setup complete. Exiting.", Colors.GREEN)
        sys.exit(0)

    # Start server
    start_server(args.host, args.port, settings_module)

if __name__ == '__main__':
    main()
