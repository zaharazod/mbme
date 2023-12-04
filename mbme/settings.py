'''
mbme project settings

    see also
https://docs.djangoproject.com/en/dev/topics/settings/
https://docs.djangoproject.com/en/dev/ref/settings/

'''

from glob import glob
from pathlib import Path
try:
    from .local_settings import *  # noqa
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent

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
    #
    'photologue',
    'sortedm2m',
    #
    'django_quill',
    #
    'simple_history',
    'mbme',
    'apps.blog.blog_v1',
    'apps.biology',
]

# ############################### mbme specific options #########
SITE_ID = 1
BLOG_HISTORY = True

# ###############################################################
AUTH_USER_MODEL = 'mbme.User'
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

ROOT_URLCONF = 'mbme.urls'

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
                'mbme.context.mbme',
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
# STATICFILES_DIRS = [
#     # BASE_DIR / 'static',
#     # BASE_DIR / 'node_modules/lightbox2/dist',
# ]

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

WSGI_APPLICATION = 'mbme.wsgi.application'

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
AUTHENTICATION_BACKENDS = [
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]
LOGIN_URL = 'mbme:login'
LOGIN_REDIRECT_URL = 'mbme:index'
LOGOUT_URL = 'mbme:logout'
LOGOUT_REDIRECT_URL = 'mbme:index'   # noqa: F405
# for extra info
SOCIAL_AUTH_FACEBOOK_SCOPE = [
    'email',
]
SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'mbme:index'

# ######### mbme ##################
BLOG_FOOTER_LINKS = (
    ('login', '/login'),
)
