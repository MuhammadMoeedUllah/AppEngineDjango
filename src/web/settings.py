import io
import os

import environ
import google.auth
from google.cloud import secretmanager
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, f'.env'))

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-8e3_hshz(f0&b24qki%9&22rplz5ky2o(*i5uxn11#^^36lvc_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

env = environ.Env(
    SECRET_KEY=(str, os.getenv("SECRET_KEY")),
    DATABASE_URL=(str, os.getenv("DATABASE_URL")),
    GS_BUCKET_NAME=(str, os.getenv("GS_BUCKET_NAME")),
)

# Attempt to load the Project ID into the environment, safely failing on error.
try:
    _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
except google.auth.exceptions.DefaultCredentialsError:
    pass
# Use local .env file in dev mode
if os.getenv("PYTHON_ENV") == "dev":
    DEBUG = True

# Use GCP secret manager in prod mode
elif os.getenv("GOOGLE_CLOUD_PROJECT", None):
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.getenv("SETTINGS_NAME", "django_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode(
        "UTF-8"
    )

    env.read_env(io.StringIO(payload))
else:
    raise Exception(
        "No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found."
    )

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'web.api',
    'web.ui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'storages'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'web.wsgi.application'


# Database
DATABASES = {"default": env.db()}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'quotesmartlocaldev',
#         'USER': 'postgres',
#         'PASSWORD': 'admin-55',
#         'HOST': '127.0.0.1',
#         'PORT': '5432'
#     }
# }

#if docker is run via CI pipeline on GAE then DATABASES["default"]["HOST"] =localhost
CLOUD_SQL_AUTH_PROXY = "localhost"
if os.getenv("DEPLOYMENT_TYPE", "None") == "local":
    CLOUD_SQL_AUTH_PROXY = "cloudsql-proxy"


# If the flag as been set, configure to use proxy
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = CLOUD_SQL_AUTH_PROXY
    DATABASES["default"]["PORT"] = 5432

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

GS_BUCKET_NAME = env("GS_BUCKET_NAME")
STATICFILES_DIRS = []
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_DEFAULT_ACL = "publicRead"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
