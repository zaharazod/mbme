from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / '.static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / '.media/'

SECRET_KEY = '8c4eb991c6dca757bdmbmbmbd77f53902352352352424242dca757bdd77f539092e29b'

DOMAINS = ['mattbarry.me','10.5.24.124']
ALLOWED_HOSTS = ['mattbarry.me',]
CSRF_TRUSTED_ORIGINS = [f'https://{d}' for d in DOMAINS]
CSRF_COOKIE_DOMAIN = DOMAINS[0]
CORS_ORIGIN_WHITELIST = DOMAINS

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': { 'service': 'mbme' }
    }
}

# social auth
SOCIAL_AUTH_GITHUB_KEY = '7da2906bd15dabbde75b'
SOCIAL_AUTH_GITHUB_SECRET = '540e0b378070b319e45cf31a840a74f28b9affa2'
# SOCIAL_AUTH_GITHUB_SCOPE = [...]
# SOCIAL_AUTH_GITHUB_REDIRECT_URL = 'https://mattbarry.me/auth/complete/github/'
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '816494379950-j8qmo09gr1elj4efi00pbutj795elnis.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'mbme:index'

FB_SETTINGS = {
    'app_id': '822000209607109',
    'secret': '9fe04bf4803ee44a804f3fefa74f72a7'
}

