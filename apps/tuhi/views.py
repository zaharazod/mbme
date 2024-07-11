from django.shortcuts import render  # , get_object_or_404
# from logging import warning
from apps.ara.decorators import context_view
from awa.models import ProjectLink


@context_view("tuhi.Page")
def view_page(request, target, *args, **kwargs):
    # from .models import Page
    icons = ProjectLink.objects.filter(icon__isnull=False)
    # warning(f"view_page({path})")
    # page = path if isinstance(path, Page) else get_object_or_404(Page, path=path)
    # warning(f"view_page({path}) -> [{page}]")
    return render(request, "pages/page.html", {"page": target, 'icons': icons})
