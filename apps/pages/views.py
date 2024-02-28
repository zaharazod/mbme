from django.shortcuts import render

def view_page(request, path):
    return render(request, 'pages/page.html', {'path':path})
