"""
Configuración del proyecto IDPetScan.
"""

import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

# --------------------------------------------------------------------
# Seguridad
# --------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "clave-insegura-solo-para-desarrollo")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Railway pone el dominio público en esta variable automáticamente
RAILWAY_PUBLIC_DOMAIN = os.getenv("RAILWAY_PUBLIC_DOMAIN")
if RAILWAY_PUBLIC_DOMAIN:
    ALLOWED_HOSTS.append(RAILWAY_PUBLIC_DOMAIN)

CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS if h not in ("127.0.0.1", "localhost")]

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# --------------------------------------------------------------------
# Apps instaladas
# --------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "cloudinary_storage",
    "django.contrib.staticfiles",
    "cloudinary",
    "accounts",
    "pets",
    "orders",
    "backoffice",
    "anymail",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --------------------------------------------------------------------
# Base de datos
# --------------------------------------------------------------------
# Railway inyecta DATABASE_URL automáticamente al agregar Postgres.
# Si no existe (desarrollo local), usa las variables sueltas o SQLite.
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
elif os.getenv("DB_NAME"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# --------------------------------------------------------------------
# Validación de contraseñas-------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internacionalización-----------------------------------------------------
LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

# Archivos estáticos y de medios----------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
if CLOUDINARY_CLOUD_NAME:
    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": CLOUDINARY_CLOUD_NAME,
        "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
        "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
    }
    STORAGES["default"] = {"BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Redirecciones de autenticación--------------------------------
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "pets:my_pets"
LOGOUT_REDIRECT_URL = "home"

# Email -------------------
if os.getenv("BREVO_API_KEY"):
    EMAIL_BACKEND = "anymail.backends.brevo.EmailBackend"
    ANYMAIL = {
        "BREVO_API_KEY": os.getenv("BREVO_API_KEY"),
    }
    DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "info@idpetscan.com")
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ADMIN_NOTIFICATION_EMAIL = os.getenv("ADMIN_NOTIFICATION_EMAIL", "admin@idpetscan.com")

WHATSAPP_BUSINESS_NUMBER = os.getenv("WHATSAPP_BUSINESS_NUMBER", "")
