from django.urls import path
from .views import post_list, post_highlight  # , post_detail
from .feeds import PostFeed

app_name = 'blog_v1'
urlpatterns = [
    path('', post_highlight, name='index'),
    path('tag/<str:tag>/', post_list, name='post-tag-list'),
    path('rss/', PostFeed(), name='rss'),
    path('<str:slug>/detail/', post_highlight,
         name='post_detail', kwargs={'full': True}),
    path('<str:slug>/', post_highlight, name='post'),
]
