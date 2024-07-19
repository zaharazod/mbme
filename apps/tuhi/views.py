from django.shortcuts import render  # , get_object_or_404
# from logging import warning
from apps.ara.decorators import context_view
from awa.models import ProjectLink


@context_view("tuhi.Page")
def view_page(request, target, *args, **kwargs):
    icons = ProjectLink.objects.filter(icon__isnull=False)
    return render(request, "pages/page.html", {"page": target, 'icons': icons})
