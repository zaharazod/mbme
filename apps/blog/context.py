from functools import cache
from .models import Post
from django.conf import settings

@cache
def blog(request):
    return {
        'blog': {
            'nav': {
                'top': Post.posts.nav_top(),
                'end': Post.posts.nav_end(),
            }
        }
    }
