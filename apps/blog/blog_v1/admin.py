from django.contrib import admin
from .models import Post, PostComment, PostContent, Tag  # , USER


class PostContentInline(admin.TabularInline):
    model = PostContent
    fields = ['content']
    fk_name = 'parent'
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    save_on_top = True
    fieldsets = (
        (None, {
            'fields': (('title', 'subtitle', 'draft'),)
        }),
        ('Details', {
            'fields': (
                ('slug', 'post_type', 'priority'),
                'tags',
                ('created_by'),
            ),
            'classes': ('collapse',)
        }),
    )
    filter_horizontal = ('tags',)
    prepopulated_fields = {'slug': ['title']}
    inlines = PostContentInline,
    search_fields = ['tags__name', 'title', 'subtitle', 'search_text']

    @admin.action(description='Publish selected posts')
    def publish_posts(self, request, queryset):
        queryset.update(draft=False)

    @admin.action(description='Unpublish selected posts')
    def unpublish_posts(self, request, queryset):
        queryset.update(draft=True)

    actions = [publish_posts, unpublish_posts]

    @admin.display(description='Tags')
    def tag_list_display(self, obj):
        return ' '.join([tag.name for tag in obj.tags.all()])

    @admin.display(description="Published?", boolean=True)
    def is_published(self, obj):
        return not obj.draft

    list_display = ['title', 'tag_list_display',
                    'is_published', 'created_by',
                    'created', 'modified']


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    fields = ('name', )
