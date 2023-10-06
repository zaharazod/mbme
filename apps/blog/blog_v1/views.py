from django.shortcuts import render, get_object_or_404  # , get_list_or_404
from .models import Post  # , PostComment, PostContent


def post_list(request, offset=0, display=10, tag=None):
    posts = Post.posts.published()
    if tag:
        posts = posts.filter(tags__name=tag)
    posts = posts.order_by('-created')[offset: offset + display]
    return render(request, 'blog_v1/post_list.html', {'posts': posts, 'tag': tag})


def post_highlight(request, slug=None, full=False):
    if slug is None:
        slug = Post.posts.published().order_by('-created').first().slug
    post = get_object_or_404(Post, slug=slug)
    # TODO: get previous/following in one query?
    previous = Post.posts.published().filter(
        created__lt=post.created).order_by('-created')[0:10]
    following = Post.posts.published().filter(
        created__gt=post.created).order_by('created')[0:10]
    return render(request, 'blog_v1/post_highlight.html', {
        'post': post,
        'previous': previous,
        'following': following,
        'full': full
    })
