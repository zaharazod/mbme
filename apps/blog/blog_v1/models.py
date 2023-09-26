from django.db import models
from auditlog.registry import auditlog
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
# from tinymce.models import HTMLField
from django_quill.fields import QuillField

USER = get_user_model()


class BlogObject(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    # TODO: fix creator (in django admin)
    creator = models.ForeignKey(USER, null=True, on_delete=models.PROTECT)

    class Meta:
        abstract = True


class Post(BlogObject):
    title = models.CharField(max_length=80)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return f'Post: {self.title[0:15]}'

    def get_absolute_url(self):
        return reverse("blog_v1:post", kwargs={"slug": self.slug})


class PostContent(BlogObject):
    post = models.ForeignKey(
        Post, related_name='contents', on_delete=models.PROTECT)
    content = QuillField()

    def __str__(self):
        return f'Post content {self.id}'


class PostComment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.PROTECT)
    parent = models.ForeignKey('PostComment', blank=True,
                               null=True, on_delete=models.PROTECT)
    content = QuillField()

    def __str__(self):
        return f'Post comment {self.id}'
