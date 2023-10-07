from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post


class PostFeed(Feed):
    title = 'mattbarry.me'
    description = 'just some guy(\'s journal)'
    MAX_LENGTH = 100

    def link(self):
        return reverse('blog_v1:index')

    def items(self):
        return Post.objects.order_by('-created')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        content = item.contents.first()
        text = content.content.plain if content else ''
        if (len(text) > PostFeed.MAX_LENGTH):
            text = text[0:PostFeed.MAX_LENGTH] + '...'
        return text
