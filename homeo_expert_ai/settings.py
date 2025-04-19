# homeo_expert_ai/settings.py

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url  # <-- ADDED IMPORT

load_dotenv()  # Loads .env file for local development

# --- Gemini API Key ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY environment variable not set!")

BASE_DIR = Path(__file__).resolve().parent.parent

# !! Keep existing SECRET_KEY for speed - CHANGE FOR PRODUCTION !!
SECRET_KEY = "django-insecure-5+k$yqcq7cs_9n-3hyj4-mj0^n192x$+3w)_ox_*r(f8-#1tk6"

# !! Keep DEBUG=True for speed & easier debugging - SET TO False FOR PRODUCTION !!
DEBUG = True

# !! Add your future Render URL here later. '*' is insecure but fastest for testing. !!
# !! Replace '*' with ['your-app-name.onrender.com', '127.0.0.1', 'localhost'] before real use !!
ALLOWED_HOSTS = ["*"]  # <-- TEMPORARY FOR SPEED

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # Whitenoise for static files - Add BEFORE staticfiles
    "whitenoise.runserver_nostatic",  # <-- ADDED
    "django.contrib.staticfiles",
    # My apps
    "core",
    "auth_app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Whitenoise Middleware - Add AFTER SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",  # <-- ADDED
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "homeo_expert_ai.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # Keep existing context processors
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Add debug context processor if needed when DEBUG=True
                "django.template.context_processors.debug",
            ],
            # Add builtins for template tags
            "builtins": [
                "core.templatetags.json_filters",  # Ensure your filters are accessible
            ],
        },
    },
]

WSGI_APPLICATION = "homeo_expert_ai.wsgi.application"

# --- Database Configuration ---
# Uses DATABASE_URL from Render environment, defaults to local SQLite
DATABASES = {
    "default": dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,  # Optional: connection pooling
    )
}

# --- Celery Configuration ---
# Uses REDIS_URL from Render environment, defaults to local Redis
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")  # <-- UPDATED
CELERY_BROKER_URL = REDIS_URL  # <-- UPDATED
CELERY_RESULT_BACKEND = REDIS_URL  # <-- UPDATED (Using same for simplicity)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

# --- Case Results Directory ---
# Path is fine, Render will handle it based on where the code runs
CASE_RESULTS_DIR = os.path.join(BASE_DIR, "case_results")
# Ensure directory exists when app starts (useful if volume isn't persistent)
os.makedirs(CASE_RESULTS_DIR, exist_ok=True)

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization (keep as is)
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Static files ---
STATIC_URL = "static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
# Important for Render + Whitenoise + collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# Tell WhiteNoise where to find files Gunicorn doesn't know about
STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"  # <-- ADDED/UPDATED
)

# Authentication settings (keep as is)
LOGIN_URL = "/auth/account/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
