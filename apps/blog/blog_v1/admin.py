from django.contrib import admin
from .models import USER, Post, PostComment, PostContent


class PostContentInline(admin.TabularInline):
    model = PostContent
    fields = ['content']
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = PostContentInline,
    fields = ['title']


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    pass
