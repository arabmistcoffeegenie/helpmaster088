import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# In production, set the DJANGO_SECRET_KEY environment variable.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-d@H%G9sL!eB3p2xF#Q8wJzR1t@k6v*Y4uM7nP0mC5qR8sT3vU")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True") == "True"

# Allowed hosts.
# If the ALLOWED_HOSTS environment variable is not set, default to local addresses.
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost,192.168.0.106").split(",")

# CSRF Trusted Origins for custom domains (set via environment variable in production)
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if os.environ.get("CSRF_TRUSTED_ORIGINS") else []

INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Your apps
    'accounts',
    'assignments',
    'jobs',
    'payments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise for static file serving in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'helpmaster.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Global templates folder
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,  # Also looks for templates in app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Required for auth views
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'helpmaster.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # Using Path object for SQLite database
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Simplified password validators for development.
AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Your static files folder at the project root
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Where static files are collected (for production)

# WhiteNoise static files storage setting for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (e.g., user uploads like assignment briefs)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Stripe API Keys
# In production, load these from environment variables.
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "pk_live_51QqxpCJdpJzxVZD9lOu4Lv9YotwZvKUapao29R9zvUAQchrQWqCgepv7e0plcxTgy2HESuwYi2DxEx0PguFgKK0x00WkiU99gh")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "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")
