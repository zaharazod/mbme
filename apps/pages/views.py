from django.shortcuts import render, get_object_or_404
from logging import warning
from .models import Page

def view_page(request, path):
    warning(f'got: {path}')
    page = path if isinstance(path, Page) else get_object_or_404(Page, path=path)
    return render(request, 'pages/page.html', {'page':page})
