from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin
from django.utils.html import mark_safe


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """Admin configuration for blog posts with Summernote and image preview."""

    list_display = ("title", "slug", "status", "created_on", "image_preview")
    search_fields = ["title", "content"]
    list_filter = ("status", "created_on")
    prepopulated_fields = {"slug": ("title",)}
    summernote_fields = ("content",)
    readonly_fields = ("image_preview",)  # Ensure the preview is non-editable

    def image_preview(self, obj):
        if obj.featured_image_file:
            return mark_safe(f'<img src="{obj.featured_image_file.url}" width="100" />')
        elif obj.featured_image_url:
            return mark_safe(f'<img src="{obj.featured_image_url}" width="100" />')
        return "-"

    image_preview.short_description = (
        "Image Preview"  # Set column name in admin
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for comments."""

    list_display = ("post", "author", "created_on", "approved")
    list_filter = ("approved", "created_on")
    search_fields = ("post__title", "author__email", "body")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        """Bulk action to approve comments."""
        queryset.update(approved=True)

    approve_comments.short_description = "Approve selected comments"