from django.shortcuts import render, get_object_or_404  # , get_list_or_404
from .models import Post, PostType  # , PostComment, PostContent


def context(**kwargs):
    ctx = {
        'nav': Post.posts.nav_pages(),
    }
    ctx.update(**kwargs)
    return ctx


def post_list(request, offset=0, display=10, tag=None):
    posts = Post.posts.published_posts()
    if tag:
        posts = posts.filter(tags__name=tag)
    posts = posts.order_by('-created')[offset: offset + display]
    return render(request, 'blog_v1/post_list.html', context(
        posts=posts, tag=tag
    ))


def post_highlight(request, slug=None, full=False):
    if slug is None:
        slug = Post.posts.published_posts().first().slug
    post = get_object_or_404(Post, slug=slug)
    # TODO: get previous/following in one query?
    previous = Post.posts.published_posts().filter(
        created__lt=post.created).order_by('-created')[0:10]
    following = Post.posts.published_posts().filter(
        created__gt=post.created).order_by('created')[0:10]
    return render(request, 'blog_v1/post_highlight.html', context(
        post=post,
        previous=previous,
        following=following,
        full=full
    ))


def page(request, slug):
    page = get_object_or_404(Post, slug=slug, post_type=PostType.PAGE)
    return render(request, 'blog_v1/page.html', context(page=page))
