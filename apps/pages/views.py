from django.shortcuts import render, get_object_or_404
from .models import Page

def view_page(request, path):
    page = get_object_or_404(Page, path=path)
    return render(request, 'pages/page.html', {'page':page})
