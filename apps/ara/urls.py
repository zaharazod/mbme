from django.urls import path
from .views import view_context

urlpatterns = [
    path("<path:path>", view_context),
    path("", view_context),
]
