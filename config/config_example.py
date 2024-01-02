# the awa config file must be
# called 'config.py' in this
# directory, and must define
# a variable 'settings', like
# this.

settings = {
    'version': 1,
    'virtual_env': '.env',
    'autoreload': False,
    'title': 'awa example website',
    'app_name': 'awa',
    'domains': ['localhost'],
    'https': False,
    'databases': {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "awa",
        },
    },
    'paths': {
        # these would have been the defaults anyway
        'admin': 'admin',
        'blog': 'blog',
        'auth': 'auth',
    },
    'apps': None,
    'urls': None,
    'secret_key': 'asdf',
    'debug': False,
    'social': {
        'redirect': 'awa:redirect',
        'github': {
            'enabled': False,
            'key': None,
            'secret': None, 
            'scope': None,
            'redirect': None,  
        },
        'google': {
            'enabled': False,
            'key': None,
            'secret': None,
        },
        'facebook': {
            'enabled': False,
            'app': None,
            'secret': None
        },
    },
}
