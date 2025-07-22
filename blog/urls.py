from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # List all blog posts
    path('', views.PostList.as_view(), name='blog'),

    # View a single blog post using its slug
    path('<slug:slug>/', views.post_detail, name="post_detail"),

    # Edit an existing comment
    path(
        '<slug:slug>/edit_comment/<int:comment_id>/',
        views.comment_edit,
        name='comment_edit',
    ),

    # Delete a comment
    path(
        '<slug:slug>/delete_comment/<int:comment_id>/',
        views.comment_delete,
        name='comment_delete',
    ),

    # Like a post
    path('<slug:slug>/like/', views.like_post, name="like_post"),
]