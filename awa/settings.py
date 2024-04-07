from glob import glob
from pathlib import Path
from awa.util import AwaConfig

BASE_DIR = Path(__file__).resolve().parent.parent
config = AwaConfig(base_path=BASE_DIR)

for k, v in config.constants.items():
    locals()[k] = v

custom_apps = config.apps or []
INSTALLED_APPS = [
    # (needs to be before admin)
    "admin_interface",
    "colorfield",
    # django defaults
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party django apps
    "guardian",
    "social_django",
    "sortedm2m",
    "django_quill",
    "simple_history",
    "storages",
    # awa modules
    "apps.mana",
    "apps.tara",
    "awa",
    "apps.tags",
    "apps.tuhi",
] + custom_apps

# SITE_ID = config.site_id or 1
WSGI_APPLICATION = "awa.wsgi.application"

scheme = "http" if not config.https else "https"

DOMAINS = sum([d for d in [p.domains for p in config.projects]], [])

ALLOWED_HOSTS = DOMAINS
CSRF_TRUSTED_ORIGINS = [f"{scheme}://{d}" for d in DOMAINS]
# CSRF_COOKIE_DOMAIN = DOMAINS[0]
CORS_ORIGIN_WHITELIST = CSRF_TRUSTED_ORIGINS
DEBUG = config.debug or False
DATABASES = config.databases.to_dict() or {}
SECRET_KEY = config.secret_key or "aWaSecRet"
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]
CSRF_USE_SESSIONS = True

AUTH_USER_MODEL = "mana.ManaUser"
GUARDIAN_MONKEY_PATCH = False
# GUARDIAN_USER_OBJ_PERMS_MODEL = 'mana.UserPermission'
# GUARDIAN_GROUP_OBJ_PERMS_MODELS = 'mana.GroupPermission'
# ANONYMOUS_USER_ID = -1
# ANONYMOUS_USER_NAME = 'nobody'
# GUARDIAN_GET_INIT_ANONYMOUS_USER = 'apps.mana.models.get_anonymous_user'
# GUARDIAN_RENDER_403 = True
# GUARDIAN_TEMPLATE_403 =

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_currentuser.middleware.ThreadLocalUserMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

ROOT_URLCONF = "awa.urls"

# TEMPLATE_DIR = BASE_DIR / 'templates'
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # FIXME to support multiple host/projects
        # "DIRS": [BASE_DIR / "sites" / f"{xxxxx}" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                # 'apps.blog.context.blog',
                "awa.context.awa",
            ],
        },
    },
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

NODE_STATIC_GLOB = BASE_DIR / "node_modules" / "*" / "dist"
STATICFILES_DIRS = glob(NODE_STATIC_GLOB.as_posix())

AWS_ACCESS_KEY_ID = config.connections.aws.key
AWS_SECRET_ACCESS_KEY = config.connections.aws.secret

QUILL_CONFIGS = {
    "default": {
        "theme": "snow",
        "modules": {
            "syntax": True,
            "toolbar": [
                [
                    {"font": []},
                    {"align": []},
                    "bold",
                    "italic",
                    "underline",
                    "strike",
                    "blockquote",
                    {"color": []},
                    {"background": []},
                ],
                ["code-block", "link"],
                ["clean"],
            ],
        },
    }
}

PASSWORD_VALIDATION = "django.contrib.auth.password_validation"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": f"{PASSWORD_VALIDATION}.UserAttributeSimilarityValidator",
    },
    {
        "NAME": f"{PASSWORD_VALIDATION}.MinimumLengthValidator",
    },
    {
        "NAME": f"{PASSWORD_VALIDATION}.CommonPasswordValidator",
    },
    {
        "NAME": f"{PASSWORD_VALIDATION}.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# #### social_django #######
# TODO: add backends dynamically based on config
AUTHENTICATION_BACKENDS = [
    "social_core.backends.facebook.FacebookOAuth2",
    "social_core.backends.github.GithubOAuth2",
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
    "apps.mana.backends.ManaBackend",
]
LOGIN_URL = "awa:login"
LOGIN_REDIRECT_URL = "awa:index"
LOGOUT_URL = "awa:logout"
LOGOUT_REDIRECT_URL = "awa:index"  # noqa: F405
# for extra info
SOCIAL_AUTH_FACEBOOK_SCOPE = [
    "email",
]
SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_URL_NAMESPACE = "social"
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "awa:index"

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.social_auth.associate_by_email",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)

# ######### awa ##################
BLOG_HISTORY = True
BLOG_FOOTER_LINKS = (("login", "/login"),)
