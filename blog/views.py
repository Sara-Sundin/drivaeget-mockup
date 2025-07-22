from django.shortcuts import (
    render, get_object_or_404, reverse, redirect
)
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from blog.models import Post, Comment
from blog.forms import CommentForm


class PostList(generic.ListView):
    """
    View to display a paginated list of published blog posts.
    """
    queryset = Post.objects.filter(status=1)
    template_name = "blog/blog.html"
    paginate_by = 6


def post_detail(request, slug):
    """
    Display an individual post along with its comments.

    Handles comment submission when a POST request is received.
    Approved comments are counted and displayed.
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(
                request,
                "Comment submitted and awaiting approval.",
                extra_tags="comment"
            )
            return HttpResponseRedirect(
                reverse("post_detail", args=[slug]) + "#message-container"
            )

    else:
        comment_form = CommentForm()

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
        },
    )


def like_post(request, slug):
    """
    Toggle like/unlike for a post.

    If the user is authenticated, they can like or unlike a post.
    A message is displayed, and the user is redirected to the post.
    """
    post = get_object_or_404(Post, slug=slug)

    if request.user.is_authenticated:
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            messages.info(
                request,
                "You unliked this post.",
                extra_tags="comment"
            )
        else:
            post.likes.add(request.user)
            messages.success(
                request,
                "You liked this post!",
                extra_tags="comment"
            )

    return redirect(reverse("post_detail", args=[slug]) + "#like-button")


def comment_edit(request, slug, comment_id):
    """
    Edit an existing comment.

    If the comment belongs to the logged-in user, they can update it.
    Updates require re-approval. Redirects based on action:
    - "Edit" → Redirects to #commentForm.
    - Updating comment → Redirects to #message-container.
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST, instance=comment)
        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False  # Require re-approval
            comment.save()
            messages.success(
                request,
                "Comment updated successfully!",
                extra_tags="comment"
            )
            return HttpResponseRedirect(
                reverse("post_detail", args=[slug]) + "#message-container"
            )
        else:
            messages.error(
                request,
                "Error updating comment!",
                extra_tags="comment"
            )

    return HttpResponseRedirect(
        reverse("post_detail", args=[slug]) + "#commentForm"
    )


def comment_delete(request, slug, comment_id):
    """
    Delete a comment.

    If the logged-in user is the author of the comment, they can delete it.
    Otherwise, an error message is displayed. Redirects to #message-container.
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.success(
            request, "Comment deleted!", extra_tags="comment"
        )
    else:
        messages.error(
            request,
            "You can only delete your own comments!",
            extra_tags="comment"
        )

    return HttpResponseRedirect(
        reverse("post_detail", args=[slug]) + "#message-container"
    )