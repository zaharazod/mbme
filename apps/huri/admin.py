from django.contrib import admin

from .models import Theme, ThemeIcon


class IconAdmin(admin.TabularInline):
    fields = ['icon', 'icon_type']
    model = ThemeIcon
    # min_num = 1
    extra = 1


class ThemeAdmin(admin.ModelAdmin):
    model = Theme
    inlines = [IconAdmin]


# admin.site.register(Theme, ThemeAdmin)
admin.site.register(Theme, ThemeAdmin)
