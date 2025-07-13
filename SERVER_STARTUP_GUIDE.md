# Kampungcuisine Server Startup Guide

This guide provides multiple ways to start your Django development server with different settings configurations.

## 🚀 Quick Start Methods

### Method 1: Direct Command Line (Recommended)

```bash
# Development server with SQLite and Tailwind
DJANGO_SETTINGS_MODULE=core.settings_dev python manage.py tailwind runserver

# Production server with PostgreSQL
python manage.py runserver --settings=core.settings_prod

# Test environment
python manage.py runserver --settings=core.settings_test

# Custom host and port with Tailwind
DJANGO_SETTINGS_MODULE=core.settings_dev python manage.py tailwind runserver 0.0.0.0:8080
```

### Method 2: Using Environment Variables

```bash
# Set environment variable for Tailwind development
export DJANGO_SETTINGS_MODULE=core.settings_dev
python manage.py tailwind runserver

# Or set for single command
DJANGO_SETTINGS_MODULE=core.settings_dev python manage.py tailwind runserver
```

### Method 3: Using the Development Script

```bash
# Simple development server
./start_dev.sh

# Custom port
./start_dev.sh 8080

# Custom host and port
./start_dev.sh 8080 0.0.0.0
```

### Method 4: Using the Management Script

```bash
# Development environment (default)
python manage_server.py

# Production environment
python manage_server.py --env prod

# Test environment  
python manage_server.py --env test

# Custom host and port
python manage_server.py --host 0.0.0.0 --port 8080

# Skip setup prompts
python manage_server.py --auto-yes

# Only setup, don't start server
python manage_server.py --setup-only
```

## 📁 Settings Files Overview

### `core.settings_dev.py` - Development
- **Database**: SQLite (`db.sqlite3`)
- **Debug**: Enabled
- **Email**: Console backend
- **Static files**: Development serving
- **Best for**: Local development

### `core.settings_prod.py` - Production
- **Database**: PostgreSQL
- **Debug**: Disabled
- **Email**: SMTP (Resend)
- **Static files**: Production serving
- **Security**: Enhanced security headers
- **Best for**: Production deployment

### `core.settings_test.py` - Testing
- **Database**: In-memory SQLite
- **Debug**: Enabled
- **Email**: Memory backend
- **Cache**: Dummy cache
- **Best for**: Running tests

## 🔧 Environment Setup

### First Time Setup

1. **Activate Virtual Environment**
   ```bash
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations**
   ```bash
   python manage.py migrate --settings=core.settings_dev
   ```

4. **Populate Sample Data**
   ```bash
   python manage.py populate_kampungcuisine --settings=core.settings_dev
   ```

5. **Create Admin User**
   ```bash
   python manage.py createsuperuser --settings=core.settings_dev
   ```

### Daily Development Workflow

```bash
# Load development environment
source dev_setup.sh

# Start development server with Tailwind
DJANGO_SETTINGS_MODULE=core.settings_dev python manage.py tailwind runserver
```

## 🌐 Server URLs

Once the server is running, you can access:

- **Main Site**: http://127.0.0.1:8000
- **Admin Panel**: http://127.0.0.1:8000/admin
- **API Endpoints**: http://127.0.0.1:8000/api/ (if applicable)

## 🗄️ Database Information

### Development Database (SQLite)
- **File**: `db.sqlite3`
- **Location**: Project root
- **Backup**: Simply copy the file

### Current Data
- **Categories**: 3 (Ready to Eat, Spice Paste, Spice Blend)
- **Products**: 16 sample Malaysian cuisine products
- **All products**: Published and ready to display

## 🐛 Troubleshooting

### Error: "relation 'products_product' does not exist"
**Cause**: Using wrong settings (PostgreSQL instead of SQLite)
**Solution**: Always use `--settings=core.settings_dev` for development

### Error: "No module named 'products'"
**Cause**: Missing `__init__.py` files or Django not recognizing the app
**Solution**: 
```bash
python manage.py check --settings=core.settings_dev
```

### Error: "Port already in use"
**Cause**: Another process is using port 8000
**Solutions**:
```bash
# Use different port
python manage.py runserver 8080 --settings=core.settings_dev

# Kill existing process
lsof -ti:8000 | xargs kill -9  # Linux/Mac
```

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📊 Settings Comparison

| Feature | Development | Production | Testing |
|---------|-------------|------------|---------|
| Database | SQLite | PostgreSQL | In-memory SQLite |
| Debug | ✅ | ❌ | ✅ |
| Static Files | Django serves | Nginx/Apache | Django serves |
| Email | Console | SMTP | Memory |
| Cache | Local | Redis | Dummy |
| Security Headers | Basic | Enhanced | Basic |
| SSL/HTTPS | Optional | Required | Not required |

## 🚀 Production Deployment Notes

When deploying to production:

1. **Environment Variables Required**:
   ```
   DB_NAME=kampungcuisine_prod
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=5432
   RESEND_API_KEY=your_resend_key
   ADMIN_URL=your_custom_admin_url
   ```

2. **Commands for Production**:
   ```bash
   python manage.py migrate --settings=core.settings_prod
   python manage.py collectstatic --settings=core.settings_prod
   python manage.py createsuperuser --settings=core.settings_prod
   ```

3. **Use WSGI Server** (not development server):
   ```bash
   gunicorn core.wsgi:application --settings=core.settings_prod
   ```

## 💡 Tips

1. **Always specify settings** for consistency
2. **Use development script** for daily work: `./start_dev.sh`
3. **Create aliases** in your shell profile:
   ```bash
   alias rundev="python manage.py runserver --settings=core.settings_dev"
   alias shell-dev="python manage.py shell --settings=core.settings_dev"
   ```
4. **Check Django status** before starting:
   ```bash
   python manage.py check --settings=core.settings_dev
   ```

## 📱 Mobile Development

To test on mobile devices:

```bash
# Allow external connections
python manage.py runserver 0.0.0.0:8000 --settings=core.settings_dev

# Access from mobile using your computer's IP
# http://192.168.1.100:8000 (replace with your IP)
```

## 🔄 Data Management

### Reset Database
```bash
rm db.sqlite3
python manage.py migrate --settings=core.settings_dev
python manage.py populate_kampungcuisine --settings=core.settings_dev
```

### Backup Database
```bash
# SQLite backup
cp db.sqlite3 backup_$(date +%Y%m%d_%H%M%S).sqlite3

# Export data as JSON
python manage.py dumpdata --settings=core.settings_dev --indent=2 > backup.json
```

### Load Data
```bash
# Load from JSON fixture
python manage.py loaddata backup.json --settings=core.settings_dev
```

---

## 🎯 Summary

**For daily development**: Use `DJANGO_SETTINGS_MODULE=core.settings_dev python manage.py tailwind runserver`

**For quick setup**: Use `./start_dev.sh`

**For comprehensive management**: Use `python manage_server.py`

**Remember**: Use `DJANGO_SETTINGS_MODULE=core.settings_dev python manage.py tailwind runserver` for development with Tailwind CSS compilation!

**Note**: The `tailwind runserver` command automatically watches for CSS changes and recompiles Tailwind CSS in development mode.