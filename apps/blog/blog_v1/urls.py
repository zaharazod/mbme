from django.urls import path
from .views import post_list, post_dispatch
from .feeds import PostFeed

app_name = 'blog_v1'
urlpatterns = [
    path('', post_dispatch, name='index'),
    path('tag/<str:tag>/', post_list, name='post-tag-list'),
    path('rss/', PostFeed(), name='rss'),
    path('<str:slug>/detail/', post_dispatch,
         name='post-detail', kwargs={'detail': True}),
    path('<str:slug>/', post_dispatch, name='post'),
]
