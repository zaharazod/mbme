from django.urls import path
from .views import post_detail, post_list

app_name = 'blog_v1'
urlpatterns = [
    path('', post_list, name='index'),
    path('<str:slug>', post_detail, name='post'),
]
