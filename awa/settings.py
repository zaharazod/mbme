from glob import glob
from pathlib import Path
from awa.util import ConfigFile

BASE_DIR = Path(__file__).resolve().parent.parent

AWA_CONFIG_PATH = BASE_DIR / 'config' / 'config.json'
AWA_CONFIG_DEFAULTS = BASE_DIR / 'awa' / 'defaults.json'

config = ConfigFile(path=AWA_CONFIG_DEFAULTS)
config.load(AWA_CONFIG_PATH)

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
DATABASES = config.databases or {}
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
storage_classes = (
    ('static', 'django.contrib.staticfiles.views.serve'),
    ('media', '')
)
storage_var_defs = (
    ('url', r'%s/'),
    ('root', r'.%s/'),
    ('type', 'external')
)
for s, _ in storage_classes:
    for v, d in storage_var_defs:
        print(s, v, d, config.storage, config.storage[s])
        val = \
            config.storage[s][v] or \
            config.storage[v] or \
            ((d % s) if r'%s' in d else d) or s
        config.storage[s][v] = val
        locals()[f'{s.upper()}_{v.upper()}'] = val

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
