settings = {
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
