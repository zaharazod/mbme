from django.apps import AppConfig


class BlogV1Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.blog.blog_v1"
    verbose_name = 'Blog v1'
