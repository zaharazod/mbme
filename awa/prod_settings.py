from pathlib import Path
from ..config.config import settings

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / '.static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / '.media/'

scheme = 'http' if not settings.get('https', True) else 'https'
DOMAINS = settings.get('domains', ['localhost'])
ALLOWED_HOSTS = DOMAINS
CSRF_TRUSTED_ORIGINS = [f'{scheme}://{d}' for d in DOMAINS]
CSRF_COOKIE_DOMAIN = DOMAINS[0]
CORS_ORIGIN_WHITELIST = DOMAINS

DEBUG = settings.get('debug', False)
DATABASES = settings.get('databases', None)
SECRET_KEY = settings.get('secret_key','aWaSecRet')

# social auth
if 'social' in settings:
    SOCIAL_AUTH_LOGIN_REDIRECT_URL = settings.get(settings['social'].get('redirect'), 'auth/redirect')
    SOCIAL_AUTH_REDIRECT_IS_HTTPS = bool(settings.get('https', True))
    if 'github' in settings['social']:
        SOCIAL_AUTH_GITHUB_KEY = settings['social']['github']['key']
        SOCIAL_AUTH_GITHUB_SECRET = settings['social']['github']['secret']
        # SOCIAL_AUTH_GITHUB_SCOPE = [...]
        # SOCIAL_AUTH_GITHUB_REDIRECT_URL = 'https://mattbarry.me/auth/complete/github/'
    if 'google' in settings['social']:
        SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = settings['social']['google']['key']
        SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = settings['social']['google']['secret']
    if 'facebook' in settings['social']:
        # not working yet
        FB_SETTINGS = {
            'app_id': None,
            'secret': None,
        }
