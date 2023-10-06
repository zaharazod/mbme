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
    prepopulated_fields = {'slug': ['title']}
    filter_horizontal = ('tags',)
    list_display = ['title', 'tag_list_display',
                    'is_published', 'created_by',
                    'created', 'modified']
    fieldsets = (
        (None, {'fields': (('title', 'subtitle', 'draft'),)}),
        ('Details', {'fields': (('created_by', 'slug'), 'tags'),
         'classes': ('collapse',)}),
    )
    search_fields = ['tags__name', 'title', 'subtitle', 'search_text']
    actions = [publish_posts, unpublish_posts]

    @admin.display(description='Tags')
    def tag_list_display(self, obj):
        return ' '.join([tag.name for tag in obj.tags.all()])

    @admin.display(description="Published?", boolean=True)
    def is_published(self, obj):
        return not obj.draft


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    fields = ('name', )
