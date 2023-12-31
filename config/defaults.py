settings = {
    'domains': ['localhost'],
    'database': {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "awa",
        },
    },
    'apps': [],
    'urls': [],
    'secret_key': 'asdf',
    'debug': False,
    'social': {
        'redirect_url': 'awa:redirect',
        'github': {
            'enabled': False,
            'key': None,
            'secret': None,    
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
