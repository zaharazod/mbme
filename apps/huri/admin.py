from django.contrib import admin

# Register your models here.
from .models import Theme, Icon


# class IconAdmin(admin.TabularInline):
#     model = Icon


# class ThemeAdmin(admin.ModelAdmin):
#     model = Theme
#     inlines = [IconAdmin]


# admin.site.register(Theme, ThemeAdmin)
admin.site.register([Theme, Icon])
