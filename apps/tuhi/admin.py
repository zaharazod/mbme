from django.contrib import admin
from .models import Page, Folder, PageSection


AUDIT_FIELDS = ["created_by", "created", "modified"]


class PageSectionAdmin(admin.StackedInline):
    model = PageSection
    fields = ("title", "content")
    extra = 0
    min_num = 1


class PageAdmin(admin.ModelAdmin):
    readonly_fields = AUDIT_FIELDS
    prepopulated_fields = {"slug": ["title"]}
    fieldsets = [
        (None, {"fields": ["title", "slug"]}),
        ("Audit", {"fields": AUDIT_FIELDS}),
    ]
    inlines = (PageSectionAdmin,)


admin.site.register(Page, PageAdmin)
admin.site.register(Folder)
