"""
Development Django settings for core project using SQLite.
"""

from .settings import *

# Override database for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Debug settings for development
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']

# Email backend for development
# Set USE_REAL_EMAIL=true to send actual emails (requires RESEND_API_KEY)
# Otherwise emails will be printed to console
USE_REAL_EMAIL = os.getenv('USE_REAL_EMAIL', 'false').lower() == 'true'

if USE_REAL_EMAIL and os.getenv('RESEND_API_KEY'):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.resend.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False
    EMAIL_HOST_USER = "resend"
    EMAIL_HOST_PASSWORD = os.getenv("RESEND_API_KEY")
    DEFAULT_FROM_EMAIL = "noreply@applikasi.tech"
    print("🔧 Development mode: Using real email backend with Resend")
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    print("🔧 Development mode: Using console email backend (emails printed to console)")
