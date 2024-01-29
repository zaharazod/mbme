from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from .models import Post, PostContent, Tag, Blip


class BlipAdmin(GuardedModelAdmin):
    pass


admin.register(Blip, BlipAdmin)


class PostContentInline(admin.TabularInline):
    model = PostContent
    fields = ['content']
    fk_name = 'parent'
    extra = 1


class PostAdmin(GuardedModelAdmin):
    save_on_top = True
    fieldsets = (
        (None, {
            'fields': (('title', 'subtitle', 'is_draft'),)
        }),
        ('Details', {
            'fields': (
                ('slug', 'post_type', 'priority'),
                'tags',
                ('created_by',),
            ),
            'classes': ('collapse',)
        }),
    )
    filter_horizontal = ('tags',)
    prepopulated_fields = {'slug': ['title']}
    inlines = PostContentInline,
    search_fields = ['tags__name', 'title', 'subtitle', 'search_text']
    list_filter = (
        'post_type',
        'is_draft',
        'tags',
    )

    @admin.action(description='Publish selected posts')
    def publish_posts(self, request, queryset):
        queryset.update(is_draft=False)

    @admin.action(description='Unpublish selected posts')
    def unpublish_posts(self, request, queryset):
        queryset.update(is_draft=True)

    @admin.action(description='Reset content ordering')
    def reset_content_order(self, request, queryset):
        for obj in queryset.all():
            ids = list([c.id for c in obj.contents.all()])
            ids.sort()
            obj.set_postcontent_order(ids)

    actions = [publish_posts, unpublish_posts, reset_content_order]

    @admin.display(description='Tags')
    def tag_list_display(self, obj):
        return ' '.join([tag.name for tag in obj.tags.all()])

    @admin.display(description="Published?", boolean=True)
    def is_published(self, obj):
        return not obj.is_draft

    list_display = ['title', 'tag_list_display',
                    'is_published', 'created_by',
                    'created', 'modified']


@admin.register(Tag)
class TagAdmin(GuardedModelAdmin):
    model = Tag
    fields = ('name', 'security_level')
