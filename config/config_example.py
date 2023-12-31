# the awa config file must be
# called 'config.py' in this
# directory, and must define
# a variable 'settings', like
# this.

settings = {
    'title': 'awa example website',
    'app_name': 'awa',
    'admin_path': '/admin',
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
