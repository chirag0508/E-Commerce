"""
Django settings for ecommerce project.
"""

from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── SECURITY ───────────────────────────────────────────────────────────────────
# In production, set SECRET_KEY as an environment variable on Render.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-kvl!fshzvxst(rh3atcx)fblsj49a1vo3ulkelv!krj0faqy(s')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']


# ─── APPLICATIONS ───────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Cloudinary for persistent media storage on Render
    'cloudinary',
    'cloudinary_storage',

    'accounts',
    'products',
    'cart',
    'orders',
    'payments',
    'reviews',
    'core',
]


# ─── MIDDLEWARE ──────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'ecommerce.urls'


# ─── TEMPLATES ───────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# ─── DATABASE ────────────────────────────────────────────────────────────────────
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}


# ─── PASSWORD VALIDATION ─────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ─── INTERNATIONALISATION ────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ─── STATIC FILES (WhiteNoise) ───────────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# ─── MEDIA FILES (Cloudinary) ────────────────────────────────────────────────────
# Cloudinary stores product images permanently — unlike Render's ephemeral disk.
# Set these three environment variables on Render's dashboard:
#   CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
    'API_KEY':    os.environ.get('CLOUDINARY_API_KEY', ''),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', ''),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# MEDIA_URL is still used in templates when running locally.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ─── USER MODEL ──────────────────────────────────────────────────────────────────
AUTH_USER_MODEL = 'accounts.User'


# ─── EMAIL (Gmail SMTP) ──────────────────────────────────────────────────────────
# Set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD as environment variables on Render.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')


# ─── RAZORPAY ────────────────────────────────────────────────────────────────────
RAZORPAY_KEY_ID     = os.environ.get('RAZORPAY_KEY_ID', 'rzp_test_SNygSauhE9vySz')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'plFcNL7bjZa7GToAr9TjqgPp')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
