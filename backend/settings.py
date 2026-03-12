"""
Django settings for backend project.
"""

from pathlib import Path
from datetime import timedelta
import socket
import os

# Obtener IP automáticamente
def get_local_ip():
    """Obtiene la IP local automáticamente"""
    try:
        # Conectar a un servidor DNS público para obtener la IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '192.168.0.9'  # Tu IP como fallback

# Obtén la IP dinámicamente
LOCAL_IP = get_local_ip()
print(f"Usando IP: {LOCAL_IP}")

BASE_DIR = Path(__file__).resolve().parent.parent

def load_dotenv(dotenv_path):
    """Carga variables desde .env sin dependencias externas."""
    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue

        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)

load_dotenv(BASE_DIR / '.env')

SECRET_KEY = 'django-insecure-o^a*^^yclag7k$t!4ryl6_-k)uc^b^@7vqjifshvohca$38o^9'
DEBUG = True

# IMPORTANTE: Para desarrollo, permitimos todas las IPs
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    LOCAL_IP,
    '192.168.0.9',  # Tu IP específica
    '192.168.0.*',  # Permite todas las IPs en esa red
    '*',  # Para desarrollo solo
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mi_app',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',  # Asegúrate de tener esto
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # DEBE SER EL PRIMERO
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CONFIGURACIÓN CORS COMPLETA
CORS_ALLOW_ALL_ORIGINS = True  # Para desarrollo, permite todo

# Lista específica de orígenes permitidos
CORS_ALLOWED_ORIGINS = [
    # Frontend en desarrollo
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # Vite/React
    "http://127.0.0.1:5173",
    
    # Backend accesos directos
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    
    # Tu IP específica
    f"http://{LOCAL_IP}:3000",
    f"http://{LOCAL_IP}:5173",
    f"http://{LOCAL_IP}:8000",
    f"http://192.168.0.9:3000",
    f"http://192.168.0.9:5173",
    f"http://192.168.0.9:8000",
]

# Para permitir cualquier IP en tu red local
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://192\.168\.0\.\d+:\d+$",  # Cualquier IP en 192.168.0.x
    r"^http://localhost:\d+$",
    r"^http://127\.0\.0\.1:\d+$",
    r"^http://0\.0\.0\.0:\d+$",
]

CORS_ALLOW_CREDENTIALS = True

# Headers y métodos permitidos
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'access-control-allow-origin',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# CSRF Configuration para desarrollo
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    f"http://{LOCAL_IP}:3000",
    f"http://192.168.0.9:3000",
]

# Para desarrollo, desactivar seguridad CSRF
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = 'Lax'

ROOT_URLCONF = 'backend.urls'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Requiere autenticación por defecto
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'mi_app.authentication.CustomJWTAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # Para probar en navegador
    ],
}

# Configuración de SimpleJWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'usuarioid',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    
    'JTI_CLAIM': 'jti',
    
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'GestionUsuariosDB',
        'USER': 'usuarioapi',
        'PASSWORD': '22_Noteveo!',
        'HOST': 'localhost',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'extra_params': "TrustServerCertificate=yes",
            'timeout': 30,
        },
    }
}

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
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

# Email
# Si faltan credenciales SMTP, usa backend de consola para no romper en desarrollo.
EMAIL_HOST = os.getenv('EMAIL_HOST', '')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'true').lower() == 'true'
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'false').lower() == 'true'
EMAIL_TIMEOUT = int(os.getenv('EMAIL_TIMEOUT', '15'))

if EMAIL_HOST and EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER or 'no-reply@backend.local')

# URL base para frontend de reset de password.
PASSWORD_RESET_URL_TEMPLATE = os.getenv(
    'PASSWORD_RESET_URL_TEMPLATE',
    'http://localhost:5173/reset-password/{token}'
)

# Logging para debug
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'corsheaders': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
