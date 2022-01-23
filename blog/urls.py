from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.all_blogs, name='all_blogs'),
    path('<int:blog_id>/', views.detail, name='detail'),
    path('<int:blog_id>/share/',
         views.post_share, name='post_share'),
    path('tag/<slug:tag_slug>/',
         views.all_blogs, name='post_list_by_tag'),
]
