from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Post, PostComment, PostContent


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog_v1/post_detail.html', {'post': post})


def post_list(request, offset=0, display=10):
    posts = Post.objects.order_by('-created')[offset: offset + display]
    return render(request, 'blog_v1/post_list.html', {'posts': posts})
