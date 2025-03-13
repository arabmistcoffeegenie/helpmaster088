import os
import logging
from pathlib import Path
from dotenv import load_dotenv  # Ensure this is installed using `pip install python-dotenv`

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ========================= Security =========================
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "your-default-secret-key")
DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1", "yes"]
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if os.getenv("CSRF_TRUSTED_ORIGINS") else []

# ========================= Installed Apps =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',  # Use the custom AppConfig
    'assignments',
    'jobs',
    'payments',
    'storages',  # AWS S3 Storage
]

# ========================= Middleware =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ Added Whitenoise Middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ========================= URL Configuration =========================
ROOT_URLCONF = 'helpmaster.urls'

# ========================= Templates Configuration =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ========================= WSGI Application =========================
WSGI_APPLICATION = 'helpmaster.wsgi.application'

# ========================= Database Configuration =========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ========================= Password Validators (Disable for Dev) =========================
AUTH_PASSWORD_VALIDATORS = []

# ========================= Localization =========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ========================= Static & Media Files =========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # ✅ Enable Whitenoise storage

# ========================= AWS S3 Storage Configuration =========================
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "eu-north-1")  # ✅ Default to eu-north-1

if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME]):
    raise ValueError("❌ AWS S3 credentials are missing! Set them in the environment.")

# ✅ AWS S3 Correct Endpoint for any region
AWS_S3_ENDPOINT_URL = f"https://s3.{AWS_S3_REGION_NAME}.amazonaws.com"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# ========================= Stripe API Configuration =========================
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

# ========================= Debugging & Logging =========================
LOG_FILE_PATH = BASE_DIR / "logs" / "django_errors.log"
os.makedirs(BASE_DIR / "logs", exist_ok=True)  # Ensure logs directory exists

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE_PATH,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# ✅ Extra Debugging Info
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(f"DEBUG Mode: {DEBUG}")
    logging.debug(f"Allowed Hosts: {ALLOWED_HOSTS}")
    logging.debug(f"AWS Access Key ID: {'SET' if AWS_ACCESS_KEY_ID else 'NOT SET'}")
    logging.debug(f"AWS Secret Access Key: {'SET' if AWS_SECRET_ACCESS_KEY else 'NOT SET'}")
    logging.debug(f"AWS Bucket: {AWS_STORAGE_BUCKET_NAME if AWS_STORAGE_BUCKET_NAME else 'NOT SET'}")
    logging.debug(f"Stripe Keys: {'SET' if STRIPE_PUBLISHABLE_KEY else 'NOT SET'}")
