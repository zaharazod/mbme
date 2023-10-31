from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import reverse
from django.db.models import Q
from django_quill.fields import QuillField
from django_currentuser.db.models import CurrentUserField
from django.contrib.contenttypes.models import ContentType


USER = get_user_model()
MAX_POST_PRIORITY = 23
MAX_SECRET = 5
NAV_PAGE_LIMIT = 5


class PostType(models.IntegerChoices):
    POST = 0, 'Post'
    PAGE = 1, 'Page'


class Tag(models.Model):
    name = models.SlugField(max_length=32, unique=True)
    security_level = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(MAX_SECRET+1)], default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog_v1:post-tag-list", kwargs={"tag": self.name})

    class Meta:
        permissions = [
            ('view_private_tag', 'Access to this tag'),
        ]


# considered implementing a custom authorization backend
# (not difficult, but this might suffice)
class BlogQuerySet(models.QuerySet):

    def tagged(self, *tags):
        return self.filter(tag__name__in=tags)

    def public(self):
        return self.clearance(0)

    def clearance(self, level):
        return self.exclude(secret__gt=level)

    def get_for_user(self, user):
        objs = self.all()
        level = getattr(user, 'security_level', 0)
        if not user.is_superuser:
            objs = objs.clearance(level)
        return objs


class BlogObject(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    created_by = CurrentUserField(related_name='blogs_created')
    modified_by = CurrentUserField(
        related_name='blogs_modified', on_update=True)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        permissions = [
            # ('view_private', 'View non-public posts'),
        ]


class PostQuerySet(BlogQuerySet):

    def published(self):
        return self.filter(draft=False)

    def draft(self):
        return self.filter(draft=True)

    def posts(self):
        return self.filter(post_type=PostType.POST)

    def pages(self):
        return self.filter(post_type=PostType.PAGE)

    def nav_pages(self):
        return self.published().pages().order_by('-priority')[0:NAV_PAGE_LIMIT]

    def page(self, slug):
        return self.pages().get(slug=slug)

    def post(self, slug):
        return self.posts().get(slug=slug)


PostManager = PostQuerySet.as_manager()


class Blip(BlogObject):
    url = models.URLField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    # screenshot preview
    title = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        unique_together = (
            ('url', 'text', 'image'),
        )


class Post(BlogObject):
    post_type = models.PositiveSmallIntegerField(
        choices=PostType.choices, default=PostType.POST)
    priority = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(MAX_POST_PRIORITY+1)], default=0)

    title = models.CharField(max_length=80)
    subtitle = models.CharField(max_length=80, blank=True)
    slug = models.SlugField(max_length=50)
    draft = models.BooleanField(default=True)
    search_text = models.TextField(blank=True)
    posts = objects = PostManager

    class Meta:
        ordering = ('-priority', '-modified')

    def __str__(self):
        return f'Post: {self.title[0:15]}'

    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)
        self.search_text = ('\n'*2).join([
            c.content.plain for c
            in self.contents.all()
        ])
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        ptype = 'post' if self.post_type is PostType.POST else 'page'
        return reverse(f'blog_v1:{ptype}', kwargs={"slug": self.slug})


class PostContent(BlogObject):
    parent = models.ForeignKey(
        Post, related_name='contents', on_delete=models.PROTECT)
    content = QuillField()

    def __str__(self):
        return f'Post content {self.id}'

    class Meta:
        order_with_respect_to = 'parent'
        # ordering = ('id',)

# class PostComment(BlogObject):
#     parent = models.ForeignKey('BlogObject', related_name="comments",
#                                blank=True, null=True, on_delete=models.PROTECT)
#     content = QuillField()

#     def __str__(self):
#         return f'Post comment {self.id}'
