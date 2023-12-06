from pathlib import Path

# templates for things that could be substituted later/in vcs
LOCAL_CONFIG = {
    'aws': {
        'access_key': 'AKIA42CT4C7RAGWDUKFC',
        'secret_key': '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',
        'region_name': 'us-east-1',
        'bucket_name': 'mattbarry.me',
    },
}

# mattbarry.me
SITE_ID = 1

BASE_DIR = Path(__file__).resolve().parent.parent

# storages
STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3.S3Storage',
        'OPTIONS': {
            'default_acl': 'public-read',
            'location': 'content/prod/',
            'querystring_auth': False,
        } | LOCAL_CONFIG['aws']
    },
    'staticfiles': {
        'BACKEND': 'storages.backends.s3.S3Storage',
        'OPTIONS': {
            'default_acl': 'public-read',
            'location': 'content/static/',
            'querystring_auth': False,
        } | LOCAL_CONFIG['aws']
    },
}

SECRET_KEY = '8c4eb9aaaaffca757bdd77f539092e29b8c4eb991c6dca757bdd77f539092e29b'

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {'service': 'mbme'}
    }
}

DOMAINS = ('mattbarry.me', '10.5.24.124')
SCHEMES = ('https',)

ALLOWED_HOSTS = DOMAINS

CSRF_TRUSTED_ORIGINS = [f'https://{d}' for d in DOMAINS]
CSRF_COOKIE_DOMAIN = DOMAINS[0]
CORS_ORIGIN_WHITELIST = DOMAINS

# social auth
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''

SOCIAL_AUTH_GITHUB_KEY = '7da2906bd15dabbde75b'
SOCIAL_AUTH_GITHUB_SECRET = '540e0b378070b319e45cf31a840a74f28b9affa2'
# SOCIAL_AUTH_GITHUB_SCOPE = [...]
# SOCIAL_AUTH_GITHUB_REDIRECT_URL = 'https://mattbarry.me/auth/complete/github/'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '816494379950-j8qmo09gr1elj4efi00pbutj795elnis.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'mbme:index'
