from django.contrib import admin

# Register your models here.
from .models import Theme, ThemeIcon


class IconAdmin(admin.TabularInline):
    model = ThemeIcon


class ThemeAdmin(admin.ModelAdmin):
    model = Theme
    inlines = [IconAdmin]


# admin.site.register(Theme, ThemeAdmin)
admin.site.register(Theme, ThemeAdmin)
