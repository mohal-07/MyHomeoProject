# homeo_expert_ai/settings.py

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url # Ensure this is imported

# Load .env file locally if it exists
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR / '.env'
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
    print("Loaded environment variables from .env file.")

# --- Gemini API Key ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY environment variable not set!")

# --- SECURITY ---
# Read from environment, use insecure fallback ONLY for local/quick demo
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-5+k$yqcq7cs_9n-3hyj4-mj0^n192x$+3w)_ox_*r(f8-#1tk6" # CHANGE THIS LATER
)
# Read DEBUG from environment, default True locally
DEBUG = os.environ.get("DEBUG", "True") == "True"

# --- Allowed Hosts & CSRF ---
# Railway injects its domain automatically via PORT env var logic usually,
# but we'll add RAILWAY_STATIC_URL hostname just in case.
ALLOWED_HOSTS = []
CSRF_TRUSTED_ORIGINS = []

# Get Railway's public domain if available (set automatically)
RAILWAY_STATIC_URL = os.environ.get('RAILWAY_STATIC_URL') # e.g., myapp-production.up.railway.app
if RAILWAY_STATIC_URL:
    ALLOWED_HOSTS.append(f'.{RAILWAY_STATIC_URL}') # Allow subdomain and root domain
    CSRF_TRUSTED_ORIGINS.append(f'https://{RAILWAY_STATIC_URL}')

# Add localhost for local dev if DEBUG is True
if DEBUG:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1'])
# If ALLOWED_HOSTS is still empty after checking Railway env var (e.g., local run)
if not ALLOWED_HOSTS:
     ALLOWED_HOSTS = ['localhost', '127.0.0.1'] # Default safe value if not on Railway

print(f"ALLOWED_HOSTS set to: {ALLOWED_HOSTS}")
print(f"CSRF_TRUSTED_ORIGINS set to: {CSRF_TRUSTED_ORIGINS}")


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic", # Add whitenoise
    "django.contrib.staticfiles",
    "core.apps.CoreConfig",
    "auth_app.apps.AuthAppConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", # Add whitenoise
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
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": [
                "core.templatetags.json_filters",
            ],
        },
    },
]

WSGI_APPLICATION = "homeo_expert_ai.wsgi.application"


# --- Database ---
# Railway provides DATABASE_URL env var
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}


# --- Celery ---
# Railway provides REDIS_URL or similar for Redis plugin
# Check Railway variable names - might be REDIS_URL, RAILWAY_REDIS_URL, etc.
# Defaulting to REDIS_URL here, adjust if Railway uses a different name
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"


# --- Case Results Directory (USING VOLUME) ---
# Railway mounts volumes at /data by default
VOLUME_MOUNT_PATH = '/data' # Default Railway volume mount point
# Check if running on Railway
if os.environ.get('RAILWAY_ENVIRONMENT'): # Railway specific env var
    CASE_RESULTS_DIR = os.path.join(VOLUME_MOUNT_PATH, 'case_results')
else:
    # Local development fallback
    CASE_RESULTS_DIR = os.path.join(BASE_DIR, 'case_results')

# Ensure the directory exists
try:
    os.makedirs(CASE_RESULTS_DIR, exist_ok=True)
    print(f"Ensured CASE_RESULTS_DIR exists: {CASE_RESULTS_DIR}")
except OSError as e:
    print(f"Warning: Could not create CASE_RESULTS_DIR '{CASE_RESULTS_DIR}': {e}")


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

# Internationalization (default)
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# --- Static files ---
STATIC_URL = "static/"
STATICFILES_DIRS = [ os.path.join(BASE_DIR, "static"), ]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles_build") # Collect static files here
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage" # Use whitenoise


# Authentication settings (default)
LOGIN_URL = "/auth/account/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Logging (optional default)
LOGGING = { ... } # Keep default or customize if needed