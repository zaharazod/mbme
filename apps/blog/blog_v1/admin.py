from django.contrib import admin
from .models import USER, Post, PostComment, PostContent, Tag


class PostContentInline(admin.TabularInline):
    model = PostContent
    fields = ['content']
    extra = 1


@admin.action(description='Publish selected posts')
def publish_posts(admin, request, queryset):
    queryset.update(draft=False)


@admin.action(description='Unpublish selected posts')
def unpublish_posts(admin, request, queryset):
    queryset.update(draft=True)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = PostContentInline,
    # FIXME: creator should autoset
    # fields = ['title', 'subtitle', 'tags', 'creator', 'slug']
    prepopulated_fields = {'slug': ['title']}
    filter_horizontal = ('tags',)
    list_display = ['title', 'creator', 'draft', 'created', 'modified']
    fieldsets = (
        (None, {'fields': (('title', 'subtitle', 'draft'),)}),
        ('Details', {'fields': (('creator', 'slug'),),
         'classes': ('collapse',)}),
    )
    actions = [publish_posts, unpublish_posts]


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    fields = ('name', )
