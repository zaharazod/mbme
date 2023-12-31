from django.template import loader, TemplateDoesNotExist, TemplateSyntaxError
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout


def default(request): return redirect('blog_v1:index')


def blog(request, slug):
    # from apps.blog.blog_v1.views import post_dispatch
    # return post_dispatch(request, slug=slug)
    return redirect('blog_v1:post', slug=slug)


def login(request):
    return render(request, 'auth/login.html') \
        if request.user.is_anonymous \
        else redirect('auth:profile')


def logout(request):
    auth_logout(request)
    return redirect('mbme:index')


def profile(request):
    return render(request, 'auth/profile.html') \
        if not request.user.is_anonymous \
        else redirect('auth:login')


def stylesheet(request, template_name):
    template_path = f'css/{template_name}.css'
    try:
        loader.get_template(template_path)
    except (TemplateSyntaxError, TemplateDoesNotExist) as e:
        raise Http404(e)
    return render(request, template_path, content_type='text/css')


def script(request, template_name):
    template_path = f'js/{template_name}.js'
    try:
        loader.get_template(template_path)
    except (TemplateSyntaxError, TemplateDoesNotExist) as e:
        raise Http404(e)
    return render(request, template_path, content_type='text/javascript')
