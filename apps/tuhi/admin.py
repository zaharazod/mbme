from django.contrib import admin

# Register your models here.
from .models import Page


class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}


admin.site.register(Page, PageAdmin)
