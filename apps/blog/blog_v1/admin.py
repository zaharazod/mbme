from django.contrib import admin
from .models import USER, Post, PostComment, PostContent, Tag


class PostContentInline(admin.TabularInline):
    model = PostContent
    fields = ['content']
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = PostContentInline,
    # FIXME: creator should autoset
    # fields = ['title', 'subtitle', 'tags', 'creator', 'slug']
    prepopulated_fields = {'slug': ['title']}
    filter_horizontal = ('tags',)
    list_display = ['title', 'creator', 'created', 'modified']
    fieldsets = (
        (None, {'fields': (('title', 'subtitle', 'draft'),)}),
        ('Details', {'fields': (('creator', 'slug'),), 'classes': ('collapse',)}),
    )


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    fields = ('name', )
