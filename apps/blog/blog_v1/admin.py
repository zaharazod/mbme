from django.contrib import admin
from .models import USER, Post, PostComment, PostContent


class PostContentInline(admin.TabularInline):
    model = PostContent
    fields = ['content']
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = PostContentInline,
    # FIXME: creator should autoset
    fields = ['title', 'creator', 'slug']
    prepopulated_fields = {'slug': ['title']}
    list_display = ['title', 'creator', 'created', 'modified']


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    pass
