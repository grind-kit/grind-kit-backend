from firebase_admin import credentials
import firebase_admin
from pathlib import Path
from decouple import config
import dj_database_url
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('DJANGO_SECRET_KEY')

DEBUG = False

# Firebase Admin SDK

# Load Firebase service account credentials from environment variables
cred = credentials.Certificate({
    "type": config("FIREBASE_TYPE"),
    "project_id": config("FIREBASE_PROJECT_ID"),
    "private_key_id": config("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": config("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": config("FIREBASE_CLIENT_EMAIL"),
    "client_id": config("FIREBASE_CLIENT_ID"),
    "auth_uri": config("FIREBASE_AUTH_URI"),
    "token_uri": config("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": config("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": config("FIREBASE_CLIENT_X509_CERT_URL")
})

# Initialize the Firebase Admin SDK
firebase_admin.initialize_app(cred)


ALLOWED_HOSTS = ['http://localhost:3000', 'localhost', 'grind-kit-backend.herokuapp.com']

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
]
CORS_ALLOW_HEADERS = ['Authorization']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'api',

    'firebase_admin',
]

AUTH_USER_MODEL = 'api.FirebaseUser'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'api.middleware.FirebaseAuthenticationMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
