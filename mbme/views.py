from django.template import loader, TemplateDoesNotExist, TemplateSyntaxError
from django.http import Http404
from django.shortcuts import render, redirect


def default(request): return redirect('blog_v1:index')


def stylesheet(request, template_name):
    template_path = f'css/{template_name}.css'
    try:
        loader.get_template(template_path)
    except (TemplateSyntaxError, TemplateDoesNotExist) as e:
        raise Http404(e)
    return render(request, template_path, content_type='text/css')
