from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from django_quill.fields import QuillField
from django_currentuser.db.models import CurrentUserField

USER = get_user_model()


class Tag(models.Model):
    name = models.SlugField(max_length=32, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog_v1:post-tag-list", kwargs={"tag": self.name})
    

class BlogObject(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    # TODO: fix creator (in django admin)
    # creator = models.ForeignKey(USER, null=True, on_delete=models.PROTECT)
    created_by = CurrentUserField(related_name='blog_created')
    updated_by = CurrentUserField(related_name='blog_updated', on_update=True)

    # class Meta:
    #     abstract = True


class PostManager(models.Manager):
    def tagged(self, *tags):
        pass

    def published(self):
        return self.filter(draft=False)


class Post(BlogObject):
    title = models.CharField(max_length=80)
    subtitle = models.CharField(max_length=80, blank=True)
    slug = models.SlugField(max_length=50)
    tags = models.ManyToManyField(Tag)
    draft = models.BooleanField(default=True)
    search_text = models.TextField(blank=True)
    posts = objects = PostManager()

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
        return reverse("blog_v1:post", kwargs={"slug": self.slug})


class PostContent(BlogObject):
    parent = models.ForeignKey(
        Post, related_name='contents', on_delete=models.PROTECT)
    content = QuillField()

    def __str__(self):
        return f'Post content {self.id}'


class PostComment(BlogObject):
    parent = models.ForeignKey('BlogObject', related_name="comments", blank=True,
                               null=True, on_delete=models.PROTECT)
    content = QuillField()

    def __str__(self):
        return f'Post comment {self.id}'
