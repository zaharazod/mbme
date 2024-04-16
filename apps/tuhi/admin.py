from django.contrib import admin

# Register your models here.
from .models import Page, Folder


class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}


admin.site.register(Page, PageAdmin)
admin.site.register(Folder)
