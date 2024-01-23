from glob import glob
from pathlib import Path
from awa.util import AwaConfig, is_a, is_dict

BASE_DIR = Path(__file__).resolve().parent.parent

AWA_CONFIG_PATH = BASE_DIR / 'config' / 'config.json'
AWA_CONFIG_DEFAULTS = BASE_DIR / 'awa' / 'defaults.json'

config = AwaConfig(base_path=BASE_DIR)

custom_apps = config.apps or []
INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #
    'social_django',
    'sortedm2m',
    'django_quill',
    'simple_history',
    'storages',
    'awa',
    'apps.blog.blog_v1',
] + custom_apps

SITE_ID = config.site_id or 1
WSGI_APPLICATION = 'awa.wsgi.application'

scheme = 'http' if not config.https else 'https'
DOMAINS = config.domains or ['localhost']
ALLOWED_HOSTS = DOMAINS
CSRF_TRUSTED_ORIGINS = [f'{scheme}://{d}' for d in DOMAINS]
CSRF_COOKIE_DOMAIN = DOMAINS[0]
CORS_ORIGIN_WHITELIST = DOMAINS
DEBUG = config.debug or False
DATABASES = config.databases.to_dict() or {}
SECRET_KEY = config.secret_key or 'aWaSecRet'
AUTH_USER_MODEL = 'awa.User'
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]
CSRF_USE_SESSIONS = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'awa.urls'

# TEMPLATE_DIR = BASE_DIR / 'templates'
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
                'social_django.context_processors.backends',
                'apps.blog.blog_v1.context.blog',
                'awa.context.awa',
            ],
        },
    },
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

NODE_STATIC_GLOB = BASE_DIR / 'node_modules' / '*' / 'dist'
STATICFILES_DIRS = [d for d in glob(NODE_STATIC_GLOB.as_posix())]

# default file storage
storage_defaults = [
    (k, v) for (k, v) in config.storage.items()
    if is_a(v, str)
]

for k, v in config.storage.items():
    if is_dict(v):
        print('found a storage type', k, v)
        for dk, dv in storage_defaults:
            v.setdefault(dk, dv)
            if r'%s' in v[dk]:
                v[dk] = v[dk] % k
            if k == 'root' and not k.startswith('/'):
                k = str(BASE_DIR / k)
            locals()[f'{k.upper()}_{dk.upper()}'] = v[dk]

AWS_ACCESS_KEY_ID = config.connections.aws.key
AWS_SECRET_ACCESS_KEY = config.connections.aws.secret

QUILL_CONFIGS = {
    'default': {
        'theme': 'snow',
        'modules': {
            'syntax': True,
            'toolbar': [
                [
                    {'font': []},
                    {'align': []},
                    'bold', 'italic', 'underline', 'strike', 'blockquote',
                    {'color': []},
                    {'background': []},
                ],
                ['code-block', 'link'],
                ['clean'],
            ]
        }
    }
}

PASSWORD_VALIDATION = 'django.contrib.auth.password_validation'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': f'{PASSWORD_VALIDATION}.UserAttributeSimilarityValidator',
    },
    {
        'NAME': f'{PASSWORD_VALIDATION}.MinimumLengthValidator',
    },
    {
        'NAME': f'{PASSWORD_VALIDATION}.CommonPasswordValidator',
    },
    {
        'NAME': f'{PASSWORD_VALIDATION}.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# #### social_django #######
# TODO: add backends dynamically based on config
AUTHENTICATION_BACKENDS = [
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]
LOGIN_URL = 'awa:login'
LOGIN_REDIRECT_URL = 'awa:index'
LOGOUT_URL = 'awa:logout'
LOGOUT_REDIRECT_URL = 'awa:index'   # noqa: F405
# for extra info
SOCIAL_AUTH_FACEBOOK_SCOPE = [
    'email',
]
SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'awa:index'

# ######### awa ##################
BLOG_HISTORY = True
BLOG_FOOTER_LINKS = (
    ('login', '/login'),
)
