from django.db import models
from auditlog.registry import auditlog
from django.contrib.auth import get_user_model
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

    def __str__(self):
        return f'Post: {self.title[0:15]}'


class PostContent(BlogObject):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    content = QuillField()

    def __str__(self):
        return f'Post content {self.id}'


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    parent = models.ForeignKey('PostComment', blank=True,
                               null=True, on_delete=models.PROTECT)
    content = QuillField()

    def __str__(self):
        return f'Post comment {self.id}'
